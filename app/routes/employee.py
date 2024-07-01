from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.decorator.decorator import login_required
from app.forms import EmployeeForm
from app.models import Employee, db


employee_bp = Blueprint("employee_bp", __name__)


@employee_bp.route("/add_employee", methods=["GET", "POST"])
@login_required
def add_employee():
    form = EmployeeForm()
    if form.validate_on_submit():
        # Combine country code and telephone number
        full_telephone_number = form.get_full_telephone_number()

        # Create a new Employee object
        new_employee = Employee(
            employee_ID=form.employee_ID.data,
            First_name=form.First_name.data,
            Last_name=form.Last_name.data,
            TelephoneNumber=full_telephone_number,
            position=form.position.data,
            location_id=form.location_id.data,
        )

        # Add to database and commit
        db.session.add(new_employee)
        db.session.commit()

        flash("Employee added successfully!", "success")
        return redirect(url_for("add_employee"))

    return render_template("add_employee.html", form=form)


@employee_bp.route("/update_employee/<employee_id>", methods=["GET", "POST"])
@login_required
def update_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    form = EmployeeForm(obj=employee)

    if request.method == "POST" and form.validate_on_submit():
        # Combine country code and telephone number
        full_telephone_number = form.get_full_telephone_number()

        employee.employee_ID = form.employee_ID.data
        employee.First_name = form.First_name.data
        employee.Last_name = form.Last_name.data
        employee.TelephoneNumber = full_telephone_number
        employee.position = form.position.data
        employee.location_id = form.location_id.data

        db.session.commit()

        flash("Employee updated successfully!", "success")
        return redirect(url_for("display_employees"))

    return render_template("update_employee.html", form=form, employee_id=employee_id)


@employee_bp.route("/delete_employee/<employee_id>", methods=["POST"])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee record deleted successfully!", "success")
    return redirect(url_for("display_employees"))


@employee_bp.route("/employees")
@login_required
def display_employees():
    employees = Employee.query.all()
    return render_template("employee_table.html", employees=employees)
