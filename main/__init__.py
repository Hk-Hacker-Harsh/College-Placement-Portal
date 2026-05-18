from flask import Flask
from flask_login import LoginManager


from .models import db, Users
from .routes.admin import admin
from .routes.auth import auth
from .routes.company import company
from .routes.student import student


def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement.db'
    db.init_app(app)

    app.config['SECRET_KEY'] = 'Harsh_K_12345'

    # Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(auth, url_prefix='/') 
    app.register_blueprint(student, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin') 
    app.register_blueprint(company, url_prefix='/company')

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app