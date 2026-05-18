from flask_login import UserMixin

from . import db

# User Table

class Users(db.Model,UserMixin):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    pass_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    profile_completed = db.Column(db.Boolean, default=False) #Checks is Onboarding Is Completed or Not.