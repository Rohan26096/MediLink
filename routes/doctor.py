from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request
)

from flask_login import (
    login_required,
    current_user
)
from forms.doctor_profile_form import DoctorEditProfileForm

from models import db
from models.doctor import Doctor
from models.appointment import Appointment
from forms.prescription_form import PrescriptionForm
from models.prescription import Prescription
from models.patient import Patient
from models.medical_record import MedicalRecord

doctor = Blueprint("doctor", __name__)


@doctor.route("/doctor/dashboard")
@login_required
def dashboard():

    doctor_profile = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    total_appointments = Appointment.query.filter_by(
        doctor_id=doctor_profile.id
    ).count()

    pending = Appointment.query.filter_by(
        doctor_id=doctor_profile.id,
        status="Pending"
    ).count()

    accepted = Appointment.query.filter_by(
        doctor_id=doctor_profile.id,
        status="Accepted"
    ).count()

    rejected = Appointment.query.filter_by(
        doctor_id=doctor_profile.id,
        status="Rejected"
    ).count()

    return render_template(
        "doctor/dashboard.html",
        total_appointments=total_appointments,
        pending=pending,
        accepted=accepted,
        rejected=rejected
    )


@doctor.route("/doctor/appointments")
@login_required
def appointments():

    doctor_profile = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    appointments = Appointment.query.filter_by(
        doctor_id=doctor_profile.id
    ).order_by(
        Appointment.appointment_date,
        Appointment.appointment_time
    ).all()

    return render_template(
        "doctor/appointments.html",
        appointments=appointments
    )


@doctor.route("/doctor/appointments/accept/<int:id>")
@login_required
def accept_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Accepted"

    db.session.commit()

    flash("Appointment accepted successfully.", "success")

    return redirect(url_for("doctor.appointments"))


@doctor.route("/doctor/appointments/reject/<int:id>")
@login_required
def reject_appointment(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Rejected"

    db.session.commit()

    flash("Appointment rejected.", "warning")

    return redirect(url_for("doctor.appointments"))


@doctor.route(
    "/doctor/appointments/consultation/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def consultation(id):

    appointment = Appointment.query.get_or_404(id)

    if request.method == "POST":

        appointment.consultation_notes = request.form.get("notes")

        appointment.status = "Completed"

        db.session.commit()

        flash("Consultation notes saved.", "success")

        return redirect(url_for("doctor.appointments"))

    return render_template(
        "doctor/consultation.html",
        appointment=appointment
    )

@doctor.route(
    "/doctor/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    doctor_profile = Doctor.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    form = DoctorEditProfileForm()

    if form.validate_on_submit():

        doctor_profile.specialization = form.specialization.data
        doctor_profile.qualification = form.qualification.data
        doctor_profile.experience = form.experience.data
        doctor_profile.department = form.department.data
        doctor_profile.consultation_fee = form.consultation_fee.data
        doctor_profile.bio = form.bio.data

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("doctor.profile")
        )

    form.specialization.data = doctor_profile.specialization
    form.qualification.data = doctor_profile.qualification
    form.experience.data = doctor_profile.experience
    form.department.data = doctor_profile.department
    form.consultation_fee.data = doctor_profile.consultation_fee
    form.bio.data = doctor_profile.bio

    return render_template(
        "doctor/profile.html",
        form=form
    )

@doctor.route(
    "/doctor/prescription/<int:appointment_id>",
    methods=["GET", "POST"]
)
@login_required
def prescription(appointment_id):

    appointment = Appointment.query.get_or_404(
        appointment_id
    )

    form = PrescriptionForm()

    prescription = Prescription.query.filter_by(
        appointment_id=appointment.id
    ).first()

    if not prescription:
        prescription = Prescription(
            appointment_id=appointment.id
        )

    if form.validate_on_submit():

        prescription.medicines = form.medicines.data
        prescription.dosage = form.dosage.data
        prescription.instructions = form.instructions.data

        db.session.add(prescription)
        db.session.commit()

        flash(
            "Prescription saved successfully.",
            "success"
        )

        return redirect(
            url_for("doctor.appointments")
        )

    elif prescription.id:

        form.medicines.data = prescription.medicines
        form.dosage.data = prescription.dosage
        form.instructions.data = prescription.instructions

    return render_template(
        "doctor/prescription.html",
        form=form,
        appointment=appointment
    )

@doctor.route("/doctor/patient/<int:patient_id>")
@login_required
def patient_history(patient_id):

    patient = Patient.query.get_or_404(patient_id)

    records = (
        MedicalRecord.query
        .filter_by(patient_id=patient.id)
        .order_by(MedicalRecord.uploaded_at.desc())
        .all()
    )

    appointments = (
        Appointment.query
        .filter_by(patient_id=patient.id)
        .order_by(Appointment.appointment_date.desc())
        .all()
    )

    prescriptions = (
        Prescription.query
        .join(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .all()
    )

    return render_template(
        "doctor/patient_history.html",
        patient=patient,
        records=records,
        appointments=appointments,
        prescriptions=prescriptions
    )