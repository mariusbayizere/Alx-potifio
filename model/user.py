# from flask_sqlalchemy import SQLAlchemy
# from . import db

# db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'user'
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     fullName = db.Column(db.String(40), nullable=False)
#     UserRole = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(30), nullable=False)

#     def __repr__(self):
#         return f'<User Id {self.user_id} Full Name {self.fullName} Email {self.email} Password {self.password}>'



#     print("To create User Table .. ")
    