from . import db

# Company Table

class Company(db.Model):
    __tablename__='company'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(25))
    logo = db.Column(db.String(255), default='default_logo.png')
    industry = db.Column(db.String(50))
    short_desc = db.Column(db.String(255))
    description = db.Column(db.Text)
    location = db.Column(db.String(100))
    hr_contact = db.Column(db.String(30))
    email = db.Column(db.String(100))
    employees_count = db.Column(db.String(20))
    website = db.Column(db.String(75))
    status = db.Column(db.String(20), default='pending') # Previously it was is_approved(Boolean), now converted to status, Possible Values: pending, approved, rejected, blacklisted 

    # Back Reference
    user = db.relationship("Users", backref=db.backref("company_data", uselist=False))