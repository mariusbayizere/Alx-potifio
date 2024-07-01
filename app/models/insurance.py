from .db import db
from sqlalchemy.orm import relationship


class Insurance(db.Model):
    __tablename__ = "insurance"

    insurance_id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False
    )
    coverage_type = db.Column(
        db.Enum("Medical_insurance", "Accident", name="coverage_type_enum"),
        nullable=False,
    )
    insurance_company = db.Column(
        db.Enum("sanlam", "RADIANT", name="insurance_company_enum"), nullable=False
    )
    premium_amount = db.Column(db.Integer, nullable=False)

    car = relationship("Car", back_populates="insurance", cascade="all, delete-orphan")

    def __init__(self, coverage_type, insurance_company, premium_amount):
        self.coverage_type = coverage_type
        self.insurance_company = insurance_company
        self.premium_amount = premium_amount

    def __repr__(self):
        return f"<Insurance {self.insurance_id} - {self.insurance_company}>"
