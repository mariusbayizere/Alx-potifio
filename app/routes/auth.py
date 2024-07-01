from flask import (
    Blueprint,
    session,
    render_template,
    redirect,
    url_for,
    flash,
)
from flask_login import logout_user, login_required
import bcrypt

from app.models.user import User
from app import db
from app.forms import (
    RegistrationForm,
    LoginForm,
)
from app.utils import login_required, send_login_notification


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    This route is responsible for allowing users to sign up if they don't have an account.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.hashpw(
            form.password.data.encode("utf-8"), bcrypt.gensalt()
        )
        new_user = User(
            fullName=form.fullName.data,
            UserRole=form.UserRole.data,
            email=form.email.data,
            password=hashed_password.decode("utf-8"),
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User registered successfully!", "success")
        return redirect(url_for("register"))
    return render_template("register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    This route is responsible for allowing users to log in.
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.checkpw(
            form.password.data.encode("utf-8"), user.password.encode("utf-8")
        ):
            session["user_id"] = user.user_id
            session.permanent = True  # Set session as permanent
            flash("Login successful!", "success")
            send_login_notification(user.email)

            if user.UserRole.lower() == "admin":
                return redirect(url_for("dashboards"))
            elif user.UserRole.lower() == "user":
                return redirect(url_for("display_cars"))
            else:
                flash("User role is not recognized.", "danger")
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    if session.get("was_once_logged_in"):
        del session["was_once_logged_in"]
    flash("You have successfully logged yourself out.", "success")
    return redirect(url_for("login"))
