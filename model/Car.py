# from . import db
# from sqlalchemy.orm import relationship
# from sqlalchemy import Enum, ForeignKey


# class Car(db.Model):
#     __tablename__ = 'car'

#     car_ID = db.Column(db.String(10), primary_key=True, nullable=False)
#     make = db.Column(Enum('TOYOTA', 'HONDA', 'FORD', name='industry'), nullable=False)
#     model = db.Column(Enum('SEDAN', 'SUV', 'TRUCK', name='car_model'), nullable=False)
#     years = db.Column(db.Integer, nullable=False)
#     color = db.Column(db.String(40), nullable=False)
#     image = db.Column(db.String(255), nullable=False, unique=True)
#     mileage = db.Column(db.Integer, nullable=False)
#     rental_price_per_day = db.Column(db.Integer, nullable=False)
#     car_status = db.Column(db.String(100), nullable=False, default='Available')

#     maintenance = relationship("Maintenance", back_populates="car", cascade="all, delete-orphan", uselist=False)
#     rentals = relationship("Rental", back_populates="car", cascade="all, delete-orphan", lazy="joined")
#     insurance_id = db.Column(db.Integer, ForeignKey('insurance.insurance_ID'))
#     insurance = relationship("Insurance", back_populates="cars")

#     def __init__(self, car_ID, make, model, years, color, image, mileage, rental_price_per_day, insurance_id):
#         self.car_ID = car_ID
#         self.make = make
#         self.model = model
#         self.years = years
#         self.color = color
#         self.image = image
#         self.mileage = mileage
#         self.rental_price_per_day = rental_price_per_day
#         self.car_status = 'Available'
#         self.insurance_id = insurance_id

















from . import db
from sqlalchemy.orm import relationship
from datetime import date
from sqlalchemy import Enum

class Car(db.Model):
    __tablename__ = 'car'

    car_ID = db.Column(db.String(10), primary_key=True, nullable=False)
    make = db.Column(db.Enum('TOYOTA', 'MERCEDES','HONDA', 'FORD','VOLKSWAGEN','BMW', name='industry'), nullable=False)
    model = db.Column(db.Enum('SEDAN', 'SUV', 'TRUCK', name='car_model'), nullable=False)
    years = db.Column(db.Integer, nullable=False)  # Year stored as integer
    color = db.Column(db.String(40), nullable=False)
    image = db.Column(db.String(255), nullable=False, unique=True)
    mileage = db.Column(db.Integer, nullable=False)
    rental_price_per_day = db.Column(db.Integer, nullable=False)
    car_status = db.Column(db.String(100), nullable=False, default='Available')

    maintenance = relationship("Maintenance", back_populates="car", cascade="all, delete-orphan", uselist=False)
    rental = relationship("Rental", back_populates="car", cascade="all, delete-orphan", lazy="joined")
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.insurance_ID'))
    insurance = relationship("Insurance", back_populates="car")

    def __init__(self, car_ID, make, model, years, color, image, mileage, rental_price_per_day, insurance_id):
        self.car_ID = car_ID
        self.make = make
        self.model = model
        self.years = years
        self.color = color
        self.image = image
        self.mileage = mileage
        self.rental_price_per_day = rental_price_per_day
        self.car_status = 'Available'  # Default value
        self.insurance_id = insurance_id
   
from flask_login import UserMixin       

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(40), nullable=False)
    UserRole = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User Id {self.user_id} Full Name {self.fullName} Email {self.email} Password {self.password}>'















# from . import db
# from sqlalchemy.orm import relationship
# from sqlalchemy import Enum

# class Car(db.Model):
#     __tablename__ = 'car'

#     car_ID = db.Column(db.String(10), primary_key=True, nullable=False)
#     make = db.Column(db.Enum('TOYOTA', 'HONDA', 'FORD', name='industry'), nullable=False)
#     model = db.Column(db.Enum('SEDAN', 'SUV', 'TRUCK', name='car_model'), nullable=False)
#     years = db.Column(db.Integer, nullable=False)
#     color = db.Column(db.String(40), nullable=False)
#     image = db.Column(db.String(255), nullable=False, unique=True)
#     mileage = db.Column(db.Integer, nullable=False)
#     rental_price_per_day = db.Column(db.Integer, nullable=False)
#     car_status = db.Column(db.String(100), nullable=False, default='Available')
#     insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.insurance_ID'))

#     rental = relationship('Rental', back_populates='car')
#     maintenance = relationship('Maintenance', back_populates='car', cascade="all, delete-orphan", uselist=False)
#     insurance = relationship('Insurance', back_populates='car')

#     def __init__(self, car_ID, make, model, years, color, image, mileage, rental_price_per_day, insurance_id):
#         self.car_ID = car_ID
#         self.make = make
#         self.model = model
#         self.years = years
#         self.color = color
#         self.image = image
#         self.mileage = mileage
#         self.rental_price_per_day = rental_price_per_day
#         self.car_status = 'Available'
#         self.insurance_id = insurance_id








