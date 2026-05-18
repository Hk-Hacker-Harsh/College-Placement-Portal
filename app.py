# This file will like controll panel of my project.
from main import create_app 
from main.models import db, admin_data
from flask import render_template


app=create_app()

@app.route('/')
def landing_page():
    return render_template('landing_page.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin_data()

    app.run(debug=True)