import os
from flask import Flask, render_template, request, session, redirect, url_for, flash, abort
from jinja2 import FileSystemLoader
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_bootstrap import Bootstrap

from globals import server, db, hasher, sess, bootstrap
from model.user import User
from model.test import Test
from model.question import Question
from model.point_category import PointCategory
from model.answer import Answer
from form.login_form import LoginForm
from form.test_form import TestForm
from form.questions_form import QuestionsForm


APP_NAME = os.getenv('APP_NAME')
SESSION_ID_KEY = 'user_id'


def login_user(user: User):
    session[SESSION_ID_KEY] = user.id

def logout_current_user():
    del session[SESSION_ID_KEY]

def get_current_user():
    return User.query.get(session[SESSION_ID_KEY]) if session.get(SESSION_ID_KEY) else None

def is_user_logged():
    return session.get(SESSION_ID_KEY) is not None

def show_if_current_path(text, route):
    return text if request.path == url_for(route) else ''


@server.context_processor
def inject_variables():
    app_name = os.getenv('APP_NAME')
    return dict(
        app_name=app_name,
        get_current_user=get_current_user,
        is_user_logged=is_user_logged,
        show_if_current_path=show_if_current_path
    )


@server.errorhandler(403)
def page_not_found(error):
   return render_template('errors/403.html', title='403'), 403


@server.errorhandler(404)
def page_not_found(error):
   return render_template('errors/404.html', title='404'), 404


@server.route('/', methods=['GET', 'POST'])
def index():
    tests = Test.query.filter_by(is_published=True).filter(Test.questions.any())
    return render_template('index.html', tests=tests)


@server.route('/login', methods=['GET', 'POST'])
def login():
    if is_user_logged():
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user and hasher.check_password_hash(user.password, password):
            login_user(user)
            flash("You've logged in successfully.")
            
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@server.route('/logout', methods=['GET', 'POST'])
def logout():
    if is_user_logged():
        logout_current_user()
        flash("You've logged out successfully.")
    
    return redirect(url_for('index'))


@server.route('/tests/create', methods=['GET', 'POST'])
def tests_create():
    if not is_user_logged():
        return redirect(url_for('index'))

    form = TestForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            test = form.to_model()
            test.created_by = get_current_user().id

            db.session.add(test)
            db.session.flush()
            db.session.commit()

            flash("New test was created, but before you publish it, let's add some questions.")
            
            return redirect(url_for('tests_questions_create', test_id=test.id))

        except Exception as e:
            db.session.rollback()
            
            flash('Something has gone wrong. Please try again.')
    
    return render_template('tests/create.html', form=form)


@server.route('/tests/<test_id>/questions/create', methods=['GET', 'POST'])
def tests_questions_create(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)
    elif not current_user_can_edit_test(test):
        abort(403)

    form = create_questions_form(test.point_categories, test.questions)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            questions = form.to_model()
            for question in questions:
                question.test_id = test_id

            Question.query.filter_by(test_id=test_id).delete()
            db.session.add_all(questions)
            db.session.flush()
            db.session.commit()

            flash("Questions were added to the test. You can publish it.")
            
            return redirect(url_for('tests_created'))

        except Exception as e:
            db.session.rollback()
            
            flash('Something has gone wrong. Please try again.')

    return render_template('tests/create_questions.html', form=form, test=test)


@server.route('/tests/created', methods=['GET', 'POST'])
def tests_created():
    user = get_current_user()
    tests = Test.query.filter_by(created_by=user.id)
    
    return render_template('tests/created.html', tests=tests)


@server.route('/tests/<test_id>/edit', methods=['GET', 'POST'])
def tests_edit(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)
    elif not current_user_can_edit_test(test):
        abort(403)

    form = TestForm.from_model(test)

    if request.method == 'POST' and form.validate_on_submit():
        try:
            test = form.to_model(test)
            current_point_categories = db.session.query(PointCategory).filter_by(test_id=test_id)

            # Delete old point categories (ie. not submitted)
            new_ids = [pc.id for pc in test.point_categories]
            for cpc in current_point_categories:
                if cpc.id not in new_ids:
                    db.session.delete(cpc)

            db.session.flush()
            db.session.commit()

            flash("New test was created, but before you publish it, let's add some questions.")
            
            return redirect(url_for('tests_created'))

        except Exception as e:
            db.session.rollback()
            
            flash('Something has gone wrong. Please try again.')

    return render_template('tests/create.html', form=form)


@server.route('/tests/<test_id>/delete', methods=['POST'])
def tests_delete(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)
    elif not current_user_can_edit_test(test):
        abort(403)

    try:
        test.point_categories
        db.session.delete(test)
        db.session.flush()
        db.session.commit()

        flash('Test was deleted successfully.')

    except Exception as e:
        return str(e)
        db.session.rollback()

        flash('Something has gone wrong. Please try again.')

    return redirect(url_for('tests_created'))


@server.route('/tests/<test_id>/publish', methods=['GET', 'POST'])
def tests_publish(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)
    elif not current_user_can_edit_test(test):
        abort(403)

    if not test.questions:
        flash('Test has no questions. To publish it, it must have at least one.')
        
        return redirect(url_for('tests_created'))

    try:
        test.is_published = True
        db.session.flush()
        db.session.commit()
        
        flash('Test is now available for others to complete.')

    except Exception as e:
        db.session.rollback()
        
        flash('Something has gone wrong. Please try again.')

    return redirect(url_for('tests_created'))


@server.route('/tests/<test_id>/unpublish', methods=['GET', 'POST'])
def tests_unpublish(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)
    elif not current_user_can_edit_test(test):
        abort(403)

    try:
        test.is_published = False
        db.session.flush()
        db.session.commit()
        
        flash('Test is now not available for others to complete.')

    except Exception as e:
        db.session.rollback()
        
        flash('Something has gone wrong. Please try again.')

    return redirect(url_for('tests_created'))

import json
@server.route('/tests/<test_id>/solve', methods=['GET', 'POST'])
def tests_solve(test_id):
    test = Test.query.get(test_id)
    if not test:
        abort(404)

    if request.method == 'POST':
        data = {}
        for key, value in request.form.items():
            parts = key.split('+')
            if len(parts) == 1:
                if key.endswith('[]'):
                    data[key[0:len(key)-2]] = request.form.getlist(key)
                else:
                    data[key] = value
            else:
                nested_dict = data.setdefault(parts[0], {})
                nested_dict[parts[1]] = value
        
        points = {id: 0 for id in [pc.id for pc in test.point_categories]}
        # return data
        for question_id in data:
            for question in test.questions:
                if question.id == question_id:
                    for answer in question.answers:
                        # Single choice
                        if question.answer_type == Question.SINGLE_CHOICE_TYPE:
                            if data[question_id] == answer.id:
                                points[answer.positive_point_category_id] += int(answer.max_points)
                                break
                        # Multiple choices
                        if question.answer_type == Question.MULTIPLE_CHOICE_TYPE:
                            if answer.id in data[question_id]:
                                points[answer.positive_point_category_id] += int(answer.max_points)
                            else:
                                points[answer.positive_point_category_id] += int(answer.min_points)
                        # Slider
                        elif question.answer_type == Question.SLIDER_TYPE:
                            for answer_id in data[question_id].keys():
                                if answer.id == answer_id:
                                    ps = int(data[question_id][answer.id])
                                    pc = answer.negative_point_category_id if ps < 0 else answer.positive_point_category_id
                                    points[pc] += abs(ps)

        points = dict(sorted(points.items(), key=lambda x: x[1], reverse=True))
        points_edited = {}
        if test.show_all_result_categories:
            points_edited = points
        else:
            # Get only highest values
            max_points = None
            for pc in points:
                if max_points is None or max_points == points[pc]:
                    points_edited[pc] = points[pc]
                    max_points = points[pc]
                else:
                    break

        return render_template('tests/result.html', test=test, points=points_edited)
    # endif

    return render_template('tests/solve.html', test=test)


def create_questions_form(point_categories, questions=None):
    form = QuestionsForm.from_model(questions) if questions else QuestionsForm()
    for question in form.questions:
        for answer in question.answers:
            answer.add_point_categories(point_categories)

    return form


def current_user_can_edit_test(test):
    user = get_current_user()
    return user and test and test.created_by == user.id


if __name__ == '__main__':
    server.run(debug=True)
