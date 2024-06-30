# from . import db
# from sqlalchemy.orm import relationship


# class Customer(db.Model):
#     __tablename__ = 'customer'
    
#     customer_ID = db.Column(db.String(10), primary_key=True, nullable=False)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     contact_information = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(250), nullable=False)
#     address = db.Column(db.String(255), nullable=False)
#     driving_license_number = db.Column(db.String(250), nullable=False)
    
#     rentals = relationship("Rental", back_populates="customer", cascade="all, delete-orphan", lazy="joined")

#     def __init__(self, customer_ID, first_name, last_name, contact_information, email, address, driving_license_number):
#         self.customer_ID = customer_ID
#         self.first_name = first_name
#         self.last_name = last_name
#         self.contact_information = contact_information
#         self.email = email
#         self.address = address
#         self.driving_license_number = driving_license_number















from . import db
from sqlalchemy.orm import relationship

class Customer(db.Model):
    __tablename__ = 'customer'
    
    customer_ID = db.Column(db.String(10), primary_key=True, nullable=False)
    First_name = db.Column(db.String(255), nullable=False)
    Last_name = db.Column(db.String(255), nullable=False)
    contact_information = db.Column(db.String(20), nullable=False)
    Email = db.Column(db.String(250), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    driving_license_number = db.Column(db.String(250), nullable=False)
    
    rentals = relationship("Rental", back_populates="customer", cascade="all, delete-orphan", lazy="joined")

    def __init__(self, customer_ID, First_name, Last_name, contact_information, Email, address, driving_license_number):
        self.customer_ID = customer_ID
        self.First_name = First_name
        self.Last_name = Last_name
        self.contact_information = contact_information
        self.Email = Email
        self.address = address
        self.driving_license_number = driving_license_number

































# from . import db
# from sqlalchemy.orm import relationship

# class Customer(db.Model):
#     __tablename__ = 'customer'

#     customer_ID = db.Column(db.String(10), primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     phone_number = db.Column(db.String(15), nullable=False)
#     address = db.Column(db.String(255), nullable=False)

#     rentals = relationship('Rental', back_populates='customer')

#     def __init__(self, customer_ID, first_name, last_name, email, phone_number, address):
#         self.customer_ID = customer_ID
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.phone_number = phone_number
#         self.address = address



