from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user
from flask_login import logout_user
from forms.auth_forms import RegisterForm, LoginForm
from models import db
from models.user import User
from utils.email import send_email
from flask_login import login_required
import logging

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        # Check if email already exists
        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data,
            role="patient"
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()
        try:
            send_email(
                user.email,
                "Welcome to MediLink",
                f"""
        Hi {user.name},

        Welcome to MediLink!

        Your account has been created successfully.

        Thank you for joining us.

        -MediLink Team
        """
            )
        except Exception:
            logging.exception("Failed to send welcome email")

        flash("Registration successful. Please login.", "success")

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )


@auth.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(
                user,
                remember=form.remember.data
            )

            flash("Login successful!", "success")

            if user.role == "patient":
                return redirect(url_for("patient.dashboard"))

            elif user.role == "doctor":
                return redirect(url_for("doctor.dashboard"))

            elif user.role == "hospital_admin":
                return redirect(url_for("hospital.dashboard"))

            elif user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            return redirect(url_for("home"))

        flash("Invalid email or password.", "danger")

    return render_template(
        "login.html",
        form=form
    )

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("home"))