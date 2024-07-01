from . import db
from sqlalchemy.orm import relationship
from datetime import date


class Maintenance(db.Model):
    __tablename__ = "maintenance"

    maintenance_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    maintenance_type = db.Column(db.String(200), nullable=False)
    maintenance_date = db.Column(db.Date, nullable=False)
    car_id = db.Column(db.String(10), db.ForeignKey("car.car_ID"), nullable=False)
    maintenance_cost = db.Column(db.Integer, nullable=False)
    employee_id = db.Column(
        db.String(10), db.ForeignKey("employee.employee_ID"), nullable=False
    )

    car = relationship("Car", back_populates="maintenance")
    employee = relationship("Employee", back_populates="maintenances")

    def __init__(
        self, maintenance_type, maintenance_date, car_id, maintenance_cost, employee_id
    ):
        self.maintenance_type = maintenance_type
        self.maintenance_date = maintenance_date
        self.car_id = car_id
        self.maintenance_cost = maintenance_cost
        self.employee_id = employee_id

    def __repr__(self):
        return f"<Maintenance {self.maintenance_id} - {self.maintenance_type} on {self.maintenance_date}>"
