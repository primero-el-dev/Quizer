from globals import db
import uuid

class Test(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_minutes = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    show_all_result_categories = db.Column(db.Boolean, default=False)
    show_results_as_percent = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='NO ACTION'), nullable=False)
    point_categories = db.relationship(
        'PointCategory', 
        backref='test', 
        lazy=False, 
        order_by='PointCategory.order', 
        cascade="all, delete-orphan"
    )
    questions = db.relationship('Question', backref='test', lazy=True, order_by='Question.order', cascade="all, delete-orphan")

    def get_max_points(self):
        points = {pc.id: 0 for pc in self.point_categories}
        for ps in [q.get_max_points(self.point_categories) for q in self.questions]:
            for k in ps.keys():
                points[k] += ps[k]

        return points

    def get_point_category(self, id):
        for pc in self.point_categories:
            if pc.id == id:
                return pc