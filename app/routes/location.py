from flask import Blueprint, flash, redirect, render_template, url_for

from app.decorator.decorator import login_required
from app.forms import LocationForm
from app.models import Location, db

location_bp = Blueprint("location", __name__)


@location_bp.route("/add_location", methods=["GET", "POST"])
def add_location():
    form = LocationForm()

    if form.validate_on_submit():
        existing_location = Location.query.filter_by(
            location_ID=form.location_ID.data
        ).first()
        if existing_location:
            flash(
                "Location ID already exists in the database. Please use a different ID.",
                "danger",
            )
        else:
            new_location = Location(
                location_ID=form.location_ID.data,
                address=form.address.data,
                contact_information=form.contact_information.data,
                operating_hours=form.operating_hours.data,
            )
            db.session.add(new_location)
            db.session.commit()
            flash("Location added successfully!", "success")
            return redirect(url_for("add_location"))

    return render_template("add_location.html", form=form)


@location_bp.route("/update_location/<location_id>", methods=["GET", "POST"])
@login_required
def update_location(location_id):
    location = Location.query.get_or_404(location_id)
    form = LocationForm(obj=location)

    if form.validate_on_submit():
        location.location_ID = form.location_ID.data
        location.address = form.address.data
        location.contact_information = form.contact_information.data
        location.operating_hours = form.operating_hours.data

        db.session.commit()
        flash("Location updated successfully!", "success")
        return redirect(url_for("display_locations"))

    return render_template("update_location.html", form=form, location_id=location_id)


@location_bp.route("/locations")
@login_required
def display_locations():
    locations = Location.query.all()
    return render_template("location_table.html", locations=locations)


@location_bp.route("/delete_location/<location_id>", methods=["POST"])
def delete_location(location_id):
    location = Location.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    flash("Location deleted successfully!", "success")
    return redirect(url_for("display_locations"))
