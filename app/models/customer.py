from sqlalchemy.orm import relationship
from .db import db


class Customer(db.Model):
    __tablename__ = "customer"

    customer_id = db.Column(db.String(10), primary_key=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    contact_information = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    address = db.Column(db.String(255), nullable=False)
    driving_license_number = db.Column(db.String(250), nullable=False)

    rentals = relationship(
        "Rental", back_populates="customer", cascade="all, delete-orphan", lazy="joined"
    )

    def __init__(
        self,
        customer_id,
        first_name,
        last_name,
        contact_information,
        email,
        address,
        driving_license_number,
    ):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.contact_information = contact_information
        self.email = email
        self.address = address
        self.driving_license_number = driving_license_number

    def __repr__(self):
        return f"<Customer {self.customer_id} - {self.first_name} {self.last_name}>"
