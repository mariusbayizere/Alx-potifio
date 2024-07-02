from flask import Blueprint, render_template

from app.decorator.decorator import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@main_bp.route("/dashboards")
@login_required
def dashboards():
    """_summary_
    this module will displaying Admin Dashboard
    Returns:
        will return the dashboard page if the request is success
    """
    return render_template("dashboard.html")


@main_bp.route("/about")
@login_required
def about():
    return render_template("about-us.html")


@main_bp.route("/contact")
@login_required
def contacts():
    return render_template("contact.html")
