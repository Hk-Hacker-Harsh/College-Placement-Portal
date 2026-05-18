# Initiave DB variable and DB Creation files.

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db=SQLAlchemy()

from .user import Users
from .student import Student
from .company import Company
from .drive import Drive
from .application import Application
from .notification import Notification


# Add Admin to DB if Does Not Exist; Convert Admin password to hash
def admin_data():
    if not Users.query.filter_by(role='admin').first():
        admin = Users(username="admin",
            pass_hash=generate_password_hash("admin"),
            role="admin")
        
        db.session.add(admin)
        db.session.commit()