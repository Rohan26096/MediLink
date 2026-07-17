from flask import Blueprint, render_template
from flask_login import login_required

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.hospital import Hospital
from models.appointment import Appointment
from sqlalchemy import or_
from flask import request
from models.prescription import Prescription
from models.medical_record import MedicalRecord

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():

    total_users = User.query.count()
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_hospitals = Hospital.query.count()
    total_appointments = Appointment.query.count()
    total_prescriptions = Prescription.query.count()
    total_medical_records = MedicalRecord.query.count()

    appointment_status = {
        "Pending": Appointment.query.filter_by(status="Pending").count(),
        "Accepted": Appointment.query.filter_by(status="Accepted").count(),
        "Rejected": Appointment.query.filter_by(status="Rejected").count(),
        "Completed": Appointment.query.filter_by(status="Completed").count()
    }
    user_labels = [
        "Patients",
        "Doctors",
        "Hospitals"
    ]

    user_counts = [
        total_patients,
        total_doctors,
        total_hospitals
    ]
    recent_users = (
        User.query
        .order_by(User.created_at.desc())
        .limit(5)
        .all()
    )

    recent_appointments = (
        Appointment.query
        .order_by(
            Appointment.appointment_date.desc(),
            Appointment.appointment_time.desc()
        )
        .limit(5)
        .all()
    )

    status_labels = list(appointment_status.keys())
    status_counts = list(appointment_status.values())

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_hospitals=total_hospitals,
        total_appointments=total_appointments,
        appointment_status=appointment_status,
        total_prescriptions=total_prescriptions,
        total_medical_records=total_medical_records,
        user_labels=user_labels,
        user_counts=user_counts,
        status_labels=status_labels,
        status_counts=status_counts,
        recent_users=recent_users,
        recent_appointments=recent_appointments
    )

@admin.route("/admin/users")
@login_required
def users():

    search = request.args.get("search", "").strip()

    users = User.query

    if search:
        users = users.filter(
            User.name.ilike(f"%{search}%") |
            User.email.ilike(f"%{search}%")
        )

    page = request.args.get("page", 1, type=int)
    per_page = 10
    users = users.order_by(
        User.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "admin/users.html",
        users=users,
        search=search
    )

@admin.route("/admin/doctors")
@login_required
def doctors():

    doctors = Doctor.query.all()

    return render_template(
        "admin/doctors.html",
        doctors=doctors
    )

@admin.route("/admin/appointments")
@login_required
def appointments():

    appointments = (
        Appointment.query
        .order_by(
            Appointment.appointment_date.desc()
        )
        .all()
    )

    return render_template(
        "admin/appointments.html",
        appointments=appointments
    )

@admin.route("/admin/search")
@login_required
def search():

    query = request.args.get("q", "").strip()

    users = []
    doctors = []
    hospitals = []
    patients = []

    if query:

        users = User.query.filter(
            or_(
                User.name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%")
            )
        ).all()

        doctors = Doctor.query.join(User).filter(
            User.name.ilike(f"%{query}%")
        ).all()

        hospitals = Hospital.query.filter(
            Hospital.name.ilike(f"%{query}%")
        ).all()

        patients = Patient.query.join(User).filter(
            User.name.ilike(f"%{query}%")
        ).all()

    return render_template(
        "admin/search.html",
        query=query,
        users=users,
        doctors=doctors,
        hospitals=hospitals,
        patients=patients
    )