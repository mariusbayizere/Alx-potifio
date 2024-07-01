from .db import db
from sqlalchemy.orm import relationship


class Employee(db.Model):
    __tablename__ = "employee"

    employee_id = db.Column(db.String(10), primary_key=True, nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    telephone_number = db.Column(db.String(20), nullable=False)
    position = db.Column(
        db.Enum("MANAGER", "STAFF", name="position_worker"), nullable=False
    )
    location_id = db.Column(db.String(10), db.ForeignKey("location.location_id"))

    rentals = relationship(
        "Rental", back_populates="employee", cascade="all, delete-orphan", lazy="joined"
    )
    location = relationship("Location", back_populates="employees")
    maintenances = relationship(
        "Maintenance",
        back_populates="employee",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __init__(
        self,
        employee_id,
        first_name,
        last_name,
        telephone_number,
        position,
        location_id,
    ):
        self.employee_id = employee_id
        self.first_name = first_name
        self.last_name = last_name
        self.telephone_number = telephone_number
        self.position = position
        self.location_id = location_id

    def __repr__(self):
        return f"<Employee {self.employee_id} - {self.first_name} {self.last_name}>"
