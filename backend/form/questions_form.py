from flask_wtf import FlaskForm
from wtforms import FormField, FieldList
from form.question_form import QuestionForm

class QuestionsForm(FlaskForm):
    questions = FieldList(FormField(QuestionForm), min_entries=1)

    def from_model(question_models):
        return QuestionsForm(questions=sorted(question_models, key=lambda q: q.order))

    def to_model(self, question_models=None):
        questions = []
        for i in range(0, len(self.questions)):
            question = None
            if question_models:
                for q in question_models:
                    if self.questions.data[i]['id'] == q.id:
                        question = self.questions[i].to_model(q)
            
            if question is None:
                question = self.questions[i].to_model()

            question.order = i + 1
            questions.append(question)

        return questions