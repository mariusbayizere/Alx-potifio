from flask import Blueprint, flash, redirect, render_template, url_for

from app.decorator.decorator import login_required
from app.forms import InsuranceForm
from app.models import Insurance, db


insurance_bp = Blueprint("insurance", __name__)


@insurance_bp.route("/add_insurance", methods=["GET", "POST"])
@login_required
def add_insurance():
    """
    add_insurance function will adding the new insurance in our system
    Returns:
    will return the add_insurance page if the Request is success
    """
    form = InsuranceForm()
    if form.validate_on_submit():
        new_insurance = Insurance(
            coverage_type=form.coverage_type.data,
            insurance_company=form.Insurance_company.data,
            premium_amount=form.premium_amount.data,
        )
        db.session.add(new_insurance)
        db.session.commit()
        flash("Insurance added successfully!", "success")
        return redirect(url_for("insurance.add_insurance"))
    return render_template("add_insurance.html", form=form)


@insurance_bp.route("/update_insurance/<int:insurance_id>", methods=["GET", "POST"])
@login_required
def update_insurance(insurance_id):

    insurance = Insurance.query.get_or_404(insurance_id)
    form = InsuranceForm(obj=insurance)

    if form.validate_on_submit():
        insurance.coverage_type = form.coverage_type.data
        insurance.Insurance_company = form.Insurance_company.data
        insurance.premium_amount = form.premium_amount.data

        db.session.commit()
        flash("Insurance updated successfully!", "success")
        return redirect(url_for("insurance.display_insurances"))

    return render_template(
        "update_insurance.html", form=form, insurance_id=insurance_id
    )


@insurance_bp.route("/delete_insurance/<int:insurance_id>", methods=["POST"])
@login_required
def delete_insurance(insurance_id):
    insurance = Insurance.query.get_or_404(insurance_id)
    db.session.delete(insurance)
    db.session.commit()
    flash("Insurance deleted successfully!", "success")
    return redirect(url_for("insurance.display_insurances"))


@insurance_bp.route("/insurances")
@login_required
def display_insurances():
    insurances = Insurance.query.all()
    return render_template("insurance_table.html", insurances=insurances)
