from . import db

# Drive Table

class Drive(db.Model):
    __tablename__='drive'
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    package = db.Column(db.Float)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending', nullable=False) # Values : pending, approved, rejected and closed

    # Back Reference
    company_details = db.relationship("Company", backref=db.backref("jobs"))