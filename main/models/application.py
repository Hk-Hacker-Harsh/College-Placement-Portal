from . import db

# Application Table

class Application(db.Model):
    __tablename__='application'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('drive.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.String(20)) # Applied / Shortlisted / Selected / Rejected

    # Back Reference
    student_details = db.relationship("Student", backref=db.backref("stu_application"))
    drive_details = db.relationship("Drive", backref=db.backref("job_application"))