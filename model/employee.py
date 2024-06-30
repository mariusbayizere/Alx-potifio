# model/employee.py
from model import db
from sqlalchemy.orm import relationship

class Employee(db.Model):
    __tablename__ = 'employee'

    employee_ID = db.Column(db.String(10), primary_key=True, nullable=False)
    First_name = db.Column(db.String(250), nullable=False)
    Last_name = db.Column(db.String (200), nullable=False)
    TelephoneNumber = db.Column(db.String(20), nullable=False)
    position = db.Column(db.Enum('MANAGER', 'STAFF', name='position_worker'), nullable=False)

    rentals = relationship("Rental", back_populates="employee", cascade="all, delete-orphan", lazy="joined")
    location_id = db.Column(db.String(10), db.ForeignKey('location.location_ID'))
    location = relationship("Location", back_populates="employees")
    maintenances = relationship("Maintenance", back_populates="employee", cascade="all, delete-orphan", lazy="joined")

    def __init__(self, employee_ID, First_name, Last_name, TelephoneNumber, position, location_id):
        self.employee_ID = employee_ID
        self.First_name = First_name
        self.Last_name = Last_name
        self.TelephoneNumber = TelephoneNumber
        self.position = position
        self.location_id = location_id













# from . import db
# from sqlalchemy.orm import relationship
# from sqlalchemy import Enum

# class Employee(db.Model):
#     __tablename__ = 'employee'

#     employee_ID = db.Column(db.String(10), primary_key=True, nullable=False)
#     First_name = db.Column(db.String(250), nullable=False)
#     Last_name = db.Column(db.String(200), nullable=False)
#     TelephoneNumber = db.Column(db.String(20), nullable=False)
#     position = db.Column(db.Enum('MANAGER', 'STAFF', name='position_worker'), nullable=False)

#     rentals = relationship("Rental", back_populates="employee", cascade="all, delete-orphan", lazy="joined")
#     location_id = db.Column(db.String(10), db.ForeignKey('location.location_ID'))
#     location = relationship("Location", back_populates="employees")
#     maintenances = relationship("Maintenance", back_populates="employee", cascade="all, delete-orphan", lazy="joined")

#     def __init__(self, employee_ID, First_name, Last_name, TelephoneNumber, position, location_id):
#         self.employee_ID = employee_ID
#         self.First_name = First_name
#         self.Last_name = Last_name
#         self.TelephoneNumber = TelephoneNumber
#         self.position = position
#         self.location_id = location_id
