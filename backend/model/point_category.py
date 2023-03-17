from globals import db
import uuid

class PointCategory(db.Model):
    __tablename__ = 'point_category'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    order = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id', ondelete='CASCADE'), nullable=False)