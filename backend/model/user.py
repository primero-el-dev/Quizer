from globals import db
import uuid

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True, default=str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)