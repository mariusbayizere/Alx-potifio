from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from app.decorator.decorator import login_required
from app.forms import RentalForm
from app.models import Car, Employee, Rental, db

rental_bp = Blueprint("rental_bp", __name__)


@rental_bp.route("/add_rental", methods=["GET", "POST"])
@login_required
def add_rental():
    form = RentalForm()
    employees = Employee.query.all()
    cars = Car.query.all()

    form.employee_id.choices = [
        (emp.employee_id, f"{emp.First_name} {emp.Last_name}") for emp in employees
    ]

    total_rental_cost = 0

    if request.method == "POST":
        if form.validate_on_submit():
            rental_start_date = form.rental_start_date.data
            return_date = form.return_date.data
            car_id = form.car_id.data

            rental_duration = (return_date - rental_start_date).days

            car = Car.query.filter_by(car_id=car_id).first()
            if not car:
                flash("Car not found!", "danger")
                return redirect(url_for("rental.add_rental"))

            employee = Employee.query.filter_by(
                employee_id=form.employee_id.data
            ).first()
            if not employee:
                flash("Employee not found!", "danger")
                return redirect(url_for("rental.add_rental"))

            print(f"Employee Position: {employee.position}")

            if employee.position.upper() != "MANAGER":
                flash("Only managers are authorized to give out cars!", "danger")
                return redirect(url_for("rental.add_rental"))

            total_rental_cost = rental_duration * car.rental_price_per_day

            new_rental = Rental(
                rental_start_date=rental_start_date,
                return_date=return_date,
                total_rental_cost=total_rental_cost,
                payment_status=form.payment_status.data,
                employee_id=form.employee_id.data,
                car_id=form.car_id.data,
                customer_id=form.customer_id.data,
            )
            db.session.add(new_rental)
            db.session.commit()
            flash("Rental added successfully!", "success")
            return redirect(url_for("rental.add_payment"))
        else:
            flash("Form validation failed. Please check your inputs.", "danger")

    return render_template(
        "add_rental.html",
        form=form,
        total_rental_cost=total_rental_cost,
        employees=employees,
        cars=cars,
    )


@rental_bp.route("/rental_table")
@login_required
def rental_table():
    rentals = Rental.query.all()  # Fetch all rentals from database

    return render_template("rental_table.html", rentals=rentals)


@rental_bp.route("/update_rental/<int:rental_id>", methods=["GET", "POST"])
@login_required
def update_rental(rental_id):
    rental = Rental.query.get_or_404(rental_id)
    form = RentalForm(obj=rental)
    employees = Employee.query.all()
    form.employee_id.choices = [
        (e.employee_id, f"{e.First_name} {e.Last_name} ({e.position})")
        for e in employees
    ]

    if request.method == "POST" and form.validate_on_submit():
        rental.rental_start_date = form.rental_start_date.data
        rental.return_date = form.return_date.data

        # Calculate rental duration in days
        rental_duration = (rental.return_date - rental.rental_start_date).days

        # Fetch car's rental price per day
        car = Car.query.filter_by(car_id=form.car_id.data).first()
        if not car:
            flash("Car not found!", "danger")
            return redirect(url_for("rental.update_rental", rental_id=rental_id))

        # Debugging info: Check rental dates and duration
        print(f"Rental Start Date: {rental.rental_start_date}")
        print(f"Return Date: {rental.return_date}")
        print(f"Rental Duration: {rental_duration} days")

        # Debugging info: Check car details
        print(f"Car ID: {form.car_id.data}")
        print(f"Car Rental Price per Day: {car.rental_price_per_day}")

        # Calculate total rental cost
        rental.total_rental_cost = rental_duration * car.rental_price_per_day

        rental.payment_status = form.payment_status.data
        rental.employee_id = form.employee_id.data
        rental.customer_id = form.customer_id.data
        rental.car_id = form.car_id.data

        db.session.commit()
        flash("Rental updated successfully!", "success")
        return redirect(url_for("rental.update_rental", rental_id=rental.rental_id))

    return render_template("rental_update.html", form=form, rental=rental)


@rental_bp.route("/get_rental_cost/<int:rental_id>", methods=["GET"])
@login_required
def get_rental_cost(rental_id):
    rental = Rental.query.filter_by(rental_id=rental_id).first()
    if rental:
        return jsonify(success=True, total_rental_cost=rental.total_rental_cost)
    else:
        return jsonify(success=False, error="Rental not found"), 404


@rental_bp.route("/delete_rental/<int:rental_id>", methods=["POST"])
@login_required
def delete_rental(rental_id):
    # Fetch the rental record by ID
    rental = Rental.query.get(rental_id)

    if rental:
        try:
            # Delete the rental record
            db.session.delete(rental)
            db.session.commit()
            flash("Rental record deleted successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting rental record: {e}", "danger")
    else:
        flash("Rental record not found!", "danger")

    return redirect(
        url_for("rental.rental_table")
    )  # Adjust the redirection as per your application's flow
