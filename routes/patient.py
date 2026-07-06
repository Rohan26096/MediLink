from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

from models import db
from models.patient import Patient
from forms.profile_forms import PatientProfileForm
from models.medical_record import MedicalRecord

patient = Blueprint("patient", __name__)


@patient.route("/patient/dashboard")
@login_required
def dashboard():

    patient_data = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    medical_records_count = 0
    appointment_count = 0
    prescription_count = 0
    profile_completion = 0
    recent_records = []

    if patient_data:

        # Count Medical Records
        medical_records_count = MedicalRecord.query.filter_by(
            patient_id=patient_data.id
        ).count()

        # Latest 5 Records
        recent_records = (
            MedicalRecord.query.filter_by(patient_id=patient_data.id)
            .order_by(MedicalRecord.uploaded_at.desc())
            .limit(5)
            .all()
        )

        # Profile Completion
        profile_fields = [
            patient_data.age,
            patient_data.gender,
            patient_data.blood_group,
            patient_data.phone,
            patient_data.address,
            patient_data.emergency_contact,
            patient_data.allergies,
            patient_data.medical_history,
        ]

        filled_fields = sum(
            1 for field in profile_fields
            if field not in (None, "")
        )

        profile_completion = int(
            (filled_fields / len(profile_fields)) * 100
        )

    return render_template(
        "patient/dashboard.html",
        medical_records_count=medical_records_count,
        appointment_count=appointment_count,
        prescription_count=prescription_count,
        profile_completion=profile_completion,
        recent_records=recent_records,
    )

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