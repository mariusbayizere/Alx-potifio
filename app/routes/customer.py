from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.decorator.decorator import login_required

from app.forms import CustomerForm
from app.models import Customer, db

customer_bp = Blueprint("customer_bp", __name__)


@customer_bp.route("/add_customer", methods=["GET", "POST"])
@login_required
def add_customer():
    customer_form = CustomerForm()

    if customer_form.validate_on_submit():
        new_customer = Customer(
            customer_ID=customer_form.customer_ID.data,
            First_name=customer_form.First_name.data,
            Last_name=customer_form.Last_name.data,
            contact_information=customer_form.contact_information.data,
            Email=customer_form.Email.data,
            address=customer_form.address.data,
            driving_license_number=customer_form.driving_license_number.data,
        )
        db.session.add(new_customer)
        db.session.commit()

        flash("Customer added successfully!", "success")
        return redirect(url_for("customer.add_customer"))

    return render_template("add_customer.html", customer_form=customer_form)


@customer_bp.route("/update_customer/<customer_id>", methods=["GET", "POST"])
@login_required
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    customer_form = CustomerForm(obj=customer)

    if request.method == "POST" and customer_form.validate_on_submit():
        customer.customer_ID = customer_form.customer_ID.data
        customer.First_name = customer_form.First_name.data
        customer.Last_name = customer_form.Last_name.data
        customer.contact_information = customer_form.contact_information.data
        customer.Email = customer_form.Email.data
        customer.address = customer_form.address.data
        customer.driving_license_number = customer_form.driving_license_number.data

        db.session.commit()

        flash("Customer updated successfully!", "success")
        return redirect(url_for("customer.display_customers"))

    return render_template(
        "update_customer.html", customer_form=customer_form, customer_id=customer_id
    )


@customer_bp.route("/delete_customer/<customer_id>", methods=["POST"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    flash("Customer record deleted successfully!", "success")
    return redirect(url_for("customer.display_customers"))


@customer_bp.route("/customers")
@login_required
def display_customers():
    customers = Customer.query.all()  # Fetch all customer records from the database
    return render_template("customer_table.html", customers=customers)
