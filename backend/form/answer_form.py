from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, StringField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length
from model.answer import Answer
import uuid
from utils import is_valid_uuid

class AnswerForm(FlaskForm):
    id = HiddenField('Id', validators=[is_valid_uuid], default=str(uuid.uuid4()))
    content = StringField('Content', validators=[
        DataRequired(), 
        Length(min=1, max=255)
    ])
    min_points = IntegerField('Points if not selected (or left on slide)', default=0)
    max_points = IntegerField('Points if selected (or right on slide)', default=0)
    first_label = StringField('First label (required, on slider on left)', validators=[
        DataRequired(), 
        Length(min=1, max=255)
    ])
    second_label = StringField('Second label (only on slider on right)', validators=[Length(max=255)])
    step = IntegerField('Point step on slider', default=1, validators=[
        DataRequired(), 
        NumberRange(min=1)
    ])
    negative_point_category_id = SelectField('Point category (left on slider)', coerce=str, choices=[], validators=[DataRequired()])
    positive_point_category_id = SelectField('Right slider point category', coerce=str, choices=[], validators=[DataRequired()])

    def from_model(model: Answer):
        return AnswerForm(
            id=model.id,
            content=model.content,
            min_points=model.min_points,
            max_points=model.max_points,
            first_label=model.first_label,
            second_label=model.second_label,
            step=model.step,
            negative_point_category_id=model.negative_point_category_id,
            positive_point_category_id=model.positive_point_category_id
        )

    def to_model(self, model=None) -> Answer:
        if not model:
            model = Answer()

        model.id = self.id.data
        model.content = self.content.data
        model.min_points = self.min_points.data
        model.max_points = self.max_points.data
        model.first_label = self.first_label.data
        model.second_label = self.second_label.data
        model.step = self.step.data
        model.negative_point_category_id = self.negative_point_category_id.data
        model.positive_point_category_id = self.positive_point_category_id.data

        return model
        
    def add_point_categories(self, point_categories):
        self.negative_point_category_id.choices = [(pc.id, pc.name) for pc in point_categories]
        self.positive_point_category_id.choices = [(pc.id, pc.name) for pc in point_categories]