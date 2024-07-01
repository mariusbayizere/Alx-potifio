from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from dotenv import load_dotenv
from app.models.user import User
from app.models.db import db
import os
import datetime

# Load environment variables from .env file
load_dotenv()

# Initialize extensions
mail = Mail()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = (
        os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS") == "True"
    )
    app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(
        seconds=int(os.getenv("PERMANENT_SESSION_LIFETIME"))
    )
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

    # Initialize extensions with the app
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()

    return app
