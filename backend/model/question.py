from globals import db
import uuid

class Question(db.Model):
    SINGLE_CHOICE_TYPE = 'single_choice'
    MULTIPLE_CHOICE_TYPE = 'multiple_choice'
    SLIDER_TYPE = 'slider'

    __tablename__ = 'question'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    order = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    answer_type = db.Column(db.String(255), nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True, order_by='Answer.order', cascade="all, delete-orphan")
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete='CASCADE'), nullable=False)

    def get_max_points(self, point_categories):
        points = {pc.id: 0 for pc in point_categories}
        for answer in self.answers:
            if self.answer_type == self.SLIDER_TYPE:
                points[answer.negative_point_category_id] += abs(answer.min_points)
                points[answer.positive_point_category_id] += answer.max_points
            else:
                points[answer.positive_point_category_id] += answer.max_points

        return points