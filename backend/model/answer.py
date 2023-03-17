from globals import db
import uuid

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    order = db.Column(db.Integer, nullable=False)
    min_points = db.Column(db.Integer, default=0)
    max_points = db.Column(db.Integer, default=0)
    first_label = db.Column(db.String(255), nullable=False)
    second_label = db.Column(db.String(255))
    step = db.Column(db.Integer, default=1)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=False)
    negative_point_category_id = db.Column(db.Integer, db.ForeignKey('point_category.id', ondelete='CASCADE'), nullable=False)
    positive_point_category_id = db.Column(db.Integer, db.ForeignKey('point_category.id', ondelete='CASCADE'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
