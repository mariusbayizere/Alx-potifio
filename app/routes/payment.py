from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.decorator.decorator import login_required
from app.forms import PaymentForm
from app.models import Payment, Rental, db, Car


payment_bp = Blueprint("payment", __name__)


@payment_bp.route("/add_payment", methods=["GET", "POST"])
@login_required
def add_payment():
    form = PaymentForm()
    if request.method == "POST":
        if form.validate_on_submit():
            rental_id = form.rental_id.data
            rental = Rental.query.filter_by(rental_id=rental_id).first()

            if not rental:
                flash("Rental not found!", "danger")
                return redirect(url_for("payment.add_payment"))

            payment_date = form.payment_date.data
            payment_method = form.payment_method.data
            amount_paid = rental.total_rental_cost  # Get the total rental cost

            # Check if card details should be included
            if payment_method in ["VISA", "CREDIT", "DEBIT"]:
                card_number = form.card_number.data
                cvv = form.cvv.data
                expiry_date = form.expiry_date.data
            else:
                card_number = None
                cvv = None
                expiry_date = None

            new_payment = Payment(
                payment_date=payment_date,
                payment_method=payment_method,
                rental_id=rental_id,
                amount_paid=amount_paid,
                card_number=card_number,
                cvv=cvv,
                expiry_date=expiry_date,
            )
            db.session.add(new_payment)

            # Update car status
            car = Car.query.filter_by(car_id=rental.car_id).first()
            if car:
                car.car_status = "Borrowed"

            # Update rental payment status
            rental.payment_status = "Success your payment Rent"

            db.session.commit()
            flash("Payment added successfully!", "success")
            return redirect(url_for("payment.add_payment"))
        else:
            flash("Form validation failed. Please check your inputs.", "danger")
    return render_template("add_payment.html", form=form)


@payment_bp.route("/update_payment/<int:payment_id>", methods=["GET", "POST"])
@login_required
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    form = PaymentForm(obj=payment)

    if form.validate_on_submit():
        payment.payment_date = form.payment_date.data
        payment.payment_method = form.payment_method.data
        payment.rental_id = form.rental_id.data
        payment.amount_paid = form.amount_paid.data

        if payment.payment_method in ["VISA", "CREDIT", "DEBIT"]:
            payment.card_number = form.card_number.data
            payment.cvv = form.cvv.data
            payment.expiry_date = form.expiry_date.data
        else:
            payment.card_number = None
            payment.cvv = None
            payment.expiry_date = None

        db.session.commit()
        flash("Payment updated successfully!", "success")
        return redirect(url_for("payment.display_payments"))

    return render_template("update_payment.html", form=form, payment_id=payment_id)


@payment_bp.route("/delete_payment/<int:payment_id>", methods=["POST"])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    flash("Payment deleted successfully!", "success")
    return redirect(url_for("payment.display_payments"))


@payment_bp.route("/payments")
@login_required
def display_payments():
    payments = Payment.query.all()
    return render_template("payment_table.html", payments=payments)
