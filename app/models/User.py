from flask_login import UserMixin
from .db import db


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(40), nullable=False)
    user_role = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Consider hashing passwords

    def __repr__(self):
        return f"<User {self.user_id} - {self.full_name}>"
