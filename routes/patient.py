from flask import (
    Blueprint,
    render_template,
    flash,
    redirect,
    url_for,
    jsonify,
    send_file,
    current_app
)
from forms.appointment_forms import AppointmentForm

from models.appointment import Appointment
from models.hospital import Hospital
from models.doctor import Doctor
from flask_login import login_required, current_user

from models import db
from models.patient import Patient
from forms.profile_forms import PatientProfileForm
from models.medical_record import MedicalRecord
from models.prescription import Prescription
from utils.email import send_email

from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet
import os
import uuid

from werkzeug.utils import secure_filename

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
    upcoming = None

    if patient_data:

        medical_records_count = MedicalRecord.query.filter_by(
            patient_id=patient_data.id
        ).count()

        appointment_count = Appointment.query.filter_by(
            patient_id=patient_data.id
        ).count()

        recent_records = (
            MedicalRecord.query.filter_by(
                patient_id=patient_data.id
            )
            .order_by(MedicalRecord.uploaded_at.desc())
            .limit(5)
            .all()
        )

        upcoming = (
            Appointment.query.filter(
                Appointment.patient_id == patient_data.id,
                Appointment.status != "Completed"
            )
            .order_by(
                Appointment.appointment_date,
                Appointment.appointment_time
            )
            .first()
        )

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
        upcoming=upcoming
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


        if form.profile_image.data:

            image = form.profile_image.data

            filename = (
                f"{uuid.uuid4().hex}_"
                f"{secure_filename(image.filename)}"
            )

            upload_path = os.path.join(
                current_app.root_path,
                "static",
                "uploads",
                "profiles"
            )

            os.makedirs(upload_path, exist_ok=True)

            image.save(
                os.path.join(upload_path, filename)
            )

            current_user.profile_image = filename

        db.session.add(patient)
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("patient.profile"))

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

@patient.route(
    "/patient/appointments/book",
    methods=["GET", "POST"]
)
@login_required
def book_appointment():

    form = AppointmentForm()

    hospitals = Hospital.query.order_by(Hospital.name).all()

    form.hospital.choices = [
        (h.id, h.name)
        for h in hospitals
    ]

    form.doctor.choices = []

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    if form.validate_on_submit():
        existing = Appointment.query.filter_by(
            doctor_id=form.doctor.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data
        ).first()

        if existing:

            flash(
                "Doctor already has an appointment at this time.",
                "danger"
            )

            return render_template(
                "patient/book_appointment.html",
                form=form
            )

        appointment = Appointment(
            patient_id=patient.id,
            hospital_id=form.hospital.data,
            doctor_id=form.doctor.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            reason=form.reason.data
        )

        db.session.add(appointment)
        db.session.commit()
        send_email(

            current_user.email,

            "Appointment Booked Successfully",

            f"""
        Hi {current_user.name},

        Your appointment has been booked successfully.

        Doctor:
        Dr. {appointment.doctor.user.name}

        Hospital:
        {appointment.hospital.name}

        Date:
        {appointment.appointment_date}

        Time:
        {appointment.appointment_time}

        Thank you for choosing MediLink.

        -MediLink Team
        """
        )

        flash(
            "Appointment booked successfully!",
            "success"
        )

        return redirect(
            url_for("patient.dashboard")
        )

    return render_template(
        "patient/book_appointment.html",
        form=form
    )
@patient.route("/patient/get-doctors/<int:hospital_id>")
@login_required
def get_doctors(hospital_id):

    doctors = Doctor.query.filter_by(
        hospital_id=hospital_id
    ).order_by(
        Doctor.specialization
    ).all()

    return jsonify([
        {
            "id": doctor.id,
            "name": doctor.user.name,
            "specialization": doctor.specialization
        }
        for doctor in doctors
    ])

@patient.route("/patient/appointments")
@login_required
def appointments():

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    if not patient:
        flash("Please complete your profile first.", "warning")
        return redirect(url_for("patient.profile"))

    appointments = Appointment.query.filter_by(
        patient_id=patient.id
    ).order_by(
        Appointment.appointment_date.desc()
    ).all()

    return render_template(
        "patient/appointments.html",
        appointments=appointments
    )

@patient.route("/patient/appointments/cancel/<int:appointment_id>")
@login_required
def cancel_appointment(appointment_id):

    appointment = Appointment.query.get_or_404(appointment_id)

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    if appointment.patient_id != patient.id:
        flash("Unauthorized action.", "danger")
        return redirect(url_for("patient.appointments"))

    if appointment.status == "Pending":
        db.session.delete(appointment)
        db.session.commit()

        flash(
            "Appointment cancelled successfully!",
            "success"
        )

    else:
        flash(
            "Only pending appointments can be cancelled.",
            "warning"
        )

    return redirect(url_for("patient.appointments"))

@patient.route("/patient/prescriptions")
@login_required
def prescriptions():

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    prescriptions = (
        Prescription.query
        .join(Appointment)
        .filter(Appointment.patient_id == patient.id)
        .order_by(Prescription.created_at.desc())
        .all()
    )

    return render_template(
        "patient/prescriptions.html",
        prescriptions=prescriptions
    )

@patient.route("/patient/prescription/pdf/<int:id>")
@login_required
def download_prescription(id):

    prescription = Prescription.query.get_or_404(id)

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b>MediLink Prescription</b>",
            styles["Title"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Doctor:</b> {prescription.appointment.doctor.user.name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Patient:</b> {prescription.appointment.patient.user.name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Medicines:</b><br/>{prescription.medicines}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Dosage:</b><br/>{prescription.dosage}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Instructions:</b><br/>{prescription.instructions}",
            styles["Normal"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Prescription.pdf",
        mimetype="application/pdf"
    )