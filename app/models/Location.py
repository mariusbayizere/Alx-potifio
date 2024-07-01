from .db import db
from sqlalchemy.orm import relationship


class Location(db.Model):
    __tablename__ = "location"

    location_id = db.Column(db.String(10), primary_key=True, nullable=False)
    address = db.Column(db.String(50), nullable=False)
    contact_information = db.Column(db.String(20), unique=True, nullable=False)
    operating_hours = db.Column(db.String(50), nullable=False)

    employees = relationship(
        "Employee",
        back_populates="location",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __init__(self, location_id, address, contact_information, operating_hours):
        self.location_id = location_id
        self.address = address
        self.contact_information = contact_information
        self.operating_hours = operating_hours

    def __repr__(self):
        return f"<Location {self.location_id} - {self.address}>"
