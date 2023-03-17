from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, TextAreaField, IntegerField, BooleanField, FormField, FieldList
from wtforms.validators import DataRequired, Optional, Length, NumberRange
from form.point_category_form import PointCategoryForm
from model.test import Test
import uuid
from utils import is_valid_uuid

class TestForm(FlaskForm):
    id = HiddenField('Id', validators=[is_valid_uuid], default=str(uuid.uuid4()))
    name = StringField('Name', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=4095)])
    estimated_minutes = IntegerField('Estimated Minutes', validators=[Optional(), NumberRange(max=300)])
    show_all_questions_on_same_page = BooleanField('Show All Questions on Same Page', default=True)
    all_time = IntegerField('All Time in minutes (set 0 for not measuring)', validators=[Optional(), NumberRange(max=300)])
    show_results = BooleanField('Show Results', default=True)
    show_all_results = BooleanField('Show All Results', default=True)
    show_all_result_categories = BooleanField('Show All Result Categories')
    show_results_as_percent = BooleanField('Show Results as Percent', default=True)
    point_categories = FieldList(FormField(PointCategoryForm), min_entries=1)

    def from_model(model: Test):
        return TestForm(
            id=model.id,
            name=model.name,
            description=model.description,
            estimated_minutes=model.estimated_minutes,
            show_all_questions_on_same_page=model.show_all_questions_on_same_page,
            all_time=model.all_time,
            show_results=model.show_results,
            show_all_results=model.show_all_results,
            show_all_result_categories=model.show_all_result_categories,
            show_results_as_percent=model.show_results_as_percent,
            point_categories=sorted(model.point_categories, key=lambda pc: pc.order)
        )

    def to_model(self, model=None):
        point_categories = []
        for i in range(0, len(self.point_categories.data)):
            point_category = None
            if model:
                for pc in model.point_categories:
                    if self.point_categories.data[i]['id'] == pc.id:
                        point_category = self.point_categories[i].to_model(pc)
            
            if point_category is None:
                point_category = self.point_categories[i].to_model()

            point_category.order = i + 1
            point_category.test_id = self.id.data
            point_categories.append(point_category)

        if model is None:
            model = Test()
        
        model.id=self.id.data
        model.name=self.name.data
        model.description=self.description.data
        model.estimated_minutes=self.estimated_minutes.data
        model.show_all_questions_on_same_page=self.show_all_questions_on_same_page.data
        model.all_time=self.all_time.data
        model.show_results=self.show_results.data
        model.show_all_results=self.show_all_results.data
        model.show_all_result_categories=self.show_all_result_categories.data
        model.show_results_as_percent=self.show_results_as_percent.data
        model.point_categories=point_categories
        
        return model