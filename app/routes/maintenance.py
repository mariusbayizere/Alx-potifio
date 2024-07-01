from flask import Blueprint, flash, redirect, render_template, url_for

from app.decorator.decorator import login_required
from app.forms import MaintenanceForm
from app.models import Maintenance, db

maintenance_bp = Blueprint("maintenance", __name__)


@maintenance_bp.route("/maintenance")
@login_required
def display_maintenance():
    maintenances = Maintenance.query.all()
    return render_template("maintenance_table.html", maintenances=maintenances)


# Add a new maintenance record
@maintenance_bp.route("/add_maintenance", methods=["GET", "POST"])
@login_required
def add_maintenance():
    form = MaintenanceForm()
    if form.validate_on_submit():
        new_maintenance = Maintenance(
            maintenance_type=form.maintenance_type.data,
            maintenance_date=form.maintenance_date.data,
            car_ID=form.car_id.data,  # Ensure this matches the correct field in your form
            maintenance_cost=form.maintenance_cost.data,
            employee_id=form.employee_id.data,  # Ensure this matches the correct field in your form
        )
        db.session.add(new_maintenance)
        db.session.commit()
        flash("Maintenance added successfully!", "success")
        return redirect(url_for("display_maintenance"))
    return render_template("add_maintenance.html", form=form)


# Update an existing maintenance record
@maintenance_bp.route(
    "/update_maintenance/<int:maintenance_id>", methods=["GET", "POST"]
)
@login_required
def update_maintenance(maintenance_id):
    maintenance = Maintenance.query.get_or_404(maintenance_id)
    form = MaintenanceForm(obj=maintenance)

    if form.validate_on_submit():
        maintenance.maintenance_type = form.maintenance_type.data
        maintenance.maintenance_date = form.maintenance_date.data
        maintenance.car_ID = form.car_id.data
        maintenance.maintenance_cost = form.maintenance_cost.data
        maintenance.employee_id = form.employee_id.data

        db.session.commit()
        flash("Maintenance updated successfully!", "success")
        return redirect(url_for("display_maintenance"))

    return render_template(
        "update_maintenance.html", form=form, maintenance_id=maintenance_id
    )


# Delete a maintenance record
@maintenance_bp.route("/delete_maintenance/<int:maintenance_id>", methods=["POST"])
def delete_maintenance(maintenance_id):
    maintenance = Maintenance.query.get_or_404(maintenance_id)
    db.session.delete(maintenance)
    db.session.commit()
    flash("Maintenance deleted successfully!", "success")
    return redirect(url_for("display_maintenance"))
