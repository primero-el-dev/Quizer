from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, SelectField, FormField, FieldList
from wtforms.validators import DataRequired, Length, NumberRange
from form.answer_form import AnswerForm
from model.question import Question
import uuid
from utils import is_valid_uuid

class QuestionForm(FlaskForm):
    id = HiddenField('Id', validators=[is_valid_uuid], default=str(uuid.uuid4()))
    content = StringField('Content', validators=[DataRequired(), Length(min=1, max=255)])
    answer_type = SelectField('Answer Type', choices=[
        ('slider', 'Slider'), 
        ('single_choice', 'Single Choice'), 
        ('multiple_choice', 'Multiple Choice')
    ], validators=[DataRequired()])
    answers = FieldList(FormField(AnswerForm), min_entries=1)

    def from_model(model: Question):
        return QuestionForm(
            id=model.id,
            content=model.content,
            answer_type=model.answer_type,
            answers=[AnswerForm.from_model(a) for a in sorted(model.answers, key=lambda a: a.order)]
        )

    def to_model(self, model=None) -> Question:
        answers = []
        for i in range(0, len(self.answers)):
            answer = None
            if model:
                for a in model.answers:
                    if a.id == self.answers[i]:
                        answer = self.answers[i].to_model(a)

            if answer is None:
                answer = self.answers[i].to_model()

            answer.order = i + 1
            answer.question_id = self.id.data
            answers.append(answer)

        return Question(
            id=self.id.data,
            content=self.content.data,
            answer_type=self.answer_type.data,
            answers=answers
        )