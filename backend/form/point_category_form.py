from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from model.point_category import PointCategory
import uuid
from utils import is_valid_uuid

class PointCategoryForm(FlaskForm):
    id = HiddenField('Id', validators=[is_valid_uuid], default=str(uuid.uuid4()))
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=255)])

    def from_model(model: PointCategory):
        return PointCategoryForm(
            id=model.id,
            name=model.name,
            description=model.description
        )

    def to_model(self, model=None):
        if model is None:
            model = PointCategory()
        
        model.id = self.id.data
        model.name = self.name.data
        model.description = self.description.data

        return model