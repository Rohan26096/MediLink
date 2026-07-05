from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

from models import db
from models.patient import Patient
from forms.profile_forms import PatientProfileForm

patient = Blueprint("patient", __name__)


@patient.route("/patient/dashboard")
@login_required
def dashboard():
    return render_template("patient/dashboard.html")

@patient.route("/patient/profile", methods=["GET", "POST"])
@login_required
def profile():

    form = PatientProfileForm()

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    if not patient:
        patient = Patient(user_id=current_user.id)

    if form.validate_on_submit():

        patient.age = form.age.data
        patient.gender = form.gender.data
        patient.blood_group = form.blood_group.data
        patient.phone = form.phone.data
        patient.address = form.address.data
        patient.emergency_contact = form.emergency_contact.data
        patient.allergies = form.allergies.data
        patient.medical_history = form.medical_history.data

        db.session.add(patient)
        db.session.commit()

        flash("Profile updated successfully!", "success")

    elif patient.id:

        form.age.data = patient.age
        form.gender.data = patient.gender
        form.blood_group.data = patient.blood_group
        form.phone.data = patient.phone
        form.address.data = patient.address
        form.emergency_contact.data = patient.emergency_contact
        form.allergies.data = patient.allergies
        form.medical_history.data = patient.medical_history

    return render_template(
        "patient/profile.html",
        form=form
    )