from .db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Rental(db.Model):
    __tablename__ = "rental"

    rental_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    rental_start_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    total_rental_cost = db.Column(db.Integer, nullable=False)
    payment_status = db.Column(db.String(255), nullable=False)

    employee_id = db.Column(
        db.String(10), db.ForeignKey("employee.employee_id"), nullable=False
    )
    employee = relationship("Employee", back_populates="rentals")

    payment = relationship(
        "Payment", uselist=False, back_populates="rental", cascade="all, delete-orphan"
    )

    car_id = db.Column(db.String(10), db.ForeignKey("car.car_id"), nullable=False)
    car = relationship("Car", back_populates="rental")

    customer_id = db.Column(
        db.String(10), db.ForeignKey("customer.customer_id"), nullable=False
    )
    customer = relationship("Customer", back_populates="rentals")

    def __init__(
        self,
        rental_start_date,
        return_date,
        total_rental_cost,
        payment_status,
        employee_id,
        car_id,
        customer_id,
    ):
        self.rental_start_date = rental_start_date
        self.return_date = return_date
        self.total_rental_cost = total_rental_cost
        self.payment_status = payment_status
        self.employee_id = employee_id
        self.car_id = car_id
        self.customer_id = customer_id

    def __repr__(self):
        return f"<Rental {self.rental_id} - Start: {self.rental_start_date}, Return: {self.return_date}, Cost: {self.total_rental_cost}>"
