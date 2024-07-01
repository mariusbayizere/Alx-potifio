import bcrypt
from flask import Blueprint, flash, redirect, render_template, url_for

from app.decorator.decorator import login_required, send_login_notification
from app.models import db, User
from app.forms import UpdatePasswordForm

user_bp = Blueprint("user", __name__)


@user_bp.route("/user.update_user/<string:email>", methods=["GET", "POST"])
@login_required
def update_user(email):
    """
    update user 's email password
    Parameters:
    email (str): The email of the user to be updated.
    Returns:
    render_template: when make Request this page will be appear
    Redirect: will be redirect to login if email password are updated
    """
    user = User.query.filter_by(email=email).first_or_404()
    form = UpdatePasswordForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.password = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        send_login_notification(user.email)

        db.session.commit()
        flash("Password Are updated successfully!", "success")
        return redirect(url_for("auth.login"))

    return render_template("user.update_user.html", form=form, email=email)
