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
from utils.email import send_email

doctor = Blueprint("doctor", __name__)


@doctor.route("/doctor/dashboard")
@login_required
def dashboard():

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    todays_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).count()

    pending = Appointment.query.filter_by(
        doctor_id=doctor.id,
        status="Pending"
    ).count()

    completed = Appointment.query.filter_by(
        doctor_id=doctor.id,
        status="Completed"
    ).count()

    total_patients = (
        db.session.query(Appointment.patient_id)
        .filter_by(doctor_id=doctor.id)
        .distinct()
        .count()
    )

    return render_template(
        "doctor/dashboard.html",
        todays_appointments=todays_appointments,
        pending=pending,
        completed=completed,
        total_patients=total_patients
    )


@doctor.route("/doctor/appointments")
@login_required
def appointments():

    doctor = Doctor.query.filter_by(
        user_id=current_user.id
    ).first()

    appointments = Appointment.query.filter_by(
        doctor_id=doctor.id
    ).order_by(
        Appointment.appointment_date.desc()
    ).all()

    return render_template(
        "doctor/appointments.html",
        appointments=appointments
    )

@doctor.route("/doctor/appointment/accept/<int:appointment_id>")
@login_required
def accept_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    appointment.status = "Accepted"

    db.session.commit()
    try:
        send_email(
            appointment.patient.user.email,
            "Appointment Accepted",
            f"""
    Hi {appointment.patient.user.name},

    Your appointment has been accepted.

    Doctor:
    Dr. {appointment.doctor.user.name}

    Date:
    {appointment.appointment_date}

    Time:
    {appointment.appointment_time}

    Please arrive 10 minutes early.

    -MediLink Team
    """
        )
    except Exception as e:
        print(e)

    flash("Appointment accepted.", "success")

    return redirect(url_for("doctor.appointments"))


@doctor.route("/doctor/appointment/reject/<int:appointment_id>")
@login_required
def reject_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    appointment.status = "Rejected"

    db.session.commit()
    try:
        send_email(

            appointment.patient.user.email,

            "Appointment Rejected",

            f"""
    Hi {appointment.patient.user.name},

    Unfortunately your appointment request
    was rejected.

    Please login to MediLink and book
    another slot.

    -MediLink Team
    """
        )
    except Exception as e:
        print(e)

    flash("Appointment rejected.", "warning")

    return redirect(url_for("doctor.appointments"))

@doctor.route("/doctor/appointment/complete/<int:appointment_id>")
@login_required
def complete_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    appointment.status = "Completed"

    db.session.commit()

    flash("Appointment completed.", "success")

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
        try:
            send_email(

                appointment.patient.user.email,

                "Prescription Uploaded",

                f"""
        Hi {appointment.patient.user.name},

        Dr. {appointment.doctor.user.name}
        has uploaded your prescription.

        Please login to MediLink
        to download it.

        Thank you.

        -MediLink Team
        """
            )
        except Exception as e:
            print(e)

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

