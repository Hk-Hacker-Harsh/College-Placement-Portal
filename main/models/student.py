from . import db

# Student Table

class Student(db.Model):
    __tablename__='student'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fname = db.Column(db.String(20))
    lname = db.Column(db.String(20))
    roll = db.Column(db.String(10), unique=True)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    degree_field = db.Column(db.String(50))
    batch = db.Column(db.Integer)
    skills = db.Column(db.Text)
    bio = db.Column(db.Text)
    resume = db.Column(db.String(255))
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    portfolio = db.Column(db.String(255))
    status = db.Column(db.String(20), default='approved') # Newly Added so that admin can blacklist students too; Values: approved, blacklisted

    # Back Reference
    user = db.relationship("Users", backref=db.backref("student_data", uselist=False))