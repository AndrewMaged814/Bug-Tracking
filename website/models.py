from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# user (one-to-many) projects
# user (one-to-many) Bug
# project (one-to-many) Bug

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    projects = db.relationship('Project', backref='user')
    bugs = db.relationship('Bug', backref='user')


 
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(500))
    status = db.Column(db.String(50))
    date_reported = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))  # The name column is defined here
    description = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bugs = db.relationship('Bug', backref='project')
