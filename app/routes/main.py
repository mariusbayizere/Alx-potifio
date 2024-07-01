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
