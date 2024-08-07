from sqlalchemy.orm import relationship
from datetime import date
from .db import db


class Payment(db.Model):
    __tablename__ = "payment"

    payment_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    payment_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(
        db.Enum("CASH", "CREDIT", "DEBIT", "VISA", name="payment_method_enum"),
        nullable=False,
    )
    rental_id = db.Column(db.Integer, db.ForeignKey("rental.rental_id"), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    card_number = db.Column(db.String(16), nullable=True)
    cvv = db.Column(db.String(3), nullable=True)
    expiry_date = db.Column(db.Date, nullable=True)

    rental = relationship("Rental", back_populates="payment")

    def __init__(
        self,
        payment_date,
        payment_method,
        rental_id,
        amount_paid,
        card_number=None,
        cvv=None,
        expiry_date=None,
    ):
        self.payment_date = payment_date
        self.payment_method = payment_method
        self.rental_id = rental_id
        self.amount_paid = amount_paid
        self.card_number = card_number
        self.cvv = cvv
        self.expiry_date = expiry_date

    def __repr__(self):
        return f"<Payment {self.payment_id} - {self.amount_paid} {self.payment_method} on {self.payment_date}>"
