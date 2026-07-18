from flask import Blueprint, render_template
from flask_login import (
    login_required,
    current_user
)
from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.hospital import Hospital
from models.appointment import Appointment
from sqlalchemy import or_
from flask import request
from models.prescription import Prescription
from models.medical_record import MedicalRecord
import csv
from io import StringIO
from flask import Response
from sqlalchemy import extract
from flask import abort

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():
    if current_user.role != "admin":
        abort(403)
    
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
    monthly_labels = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    monthly_counts = []

    for month in range(1, 13):

        count = Appointment.query.filter(
            extract("month", Appointment.appointment_date) == month
        ).count()

        monthly_counts.append(count)

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
        recent_appointments=recent_appointments,
        monthly_labels=monthly_labels,
        monthly_counts=monthly_counts
    )

@admin.route("/admin/users")
@login_required
def users():
    if current_user.role != "admin":
        abort(403)

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
    if current_user.role != "admin":
        abort(403)

    doctors = Doctor.query.all()

    return render_template(
        "admin/doctors.html",
        doctors=doctors
    )

@admin.route("/admin/appointments")
@login_required
def appointments():
    if current_user.role != "admin":
        abort(403)

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
    if current_user.role != "admin":
        abort(403)

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

@admin.route("/admin/export/users")
@login_required
def export_users():
    if current_user.role != "admin":
        abort(403)

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Name",
        "Email",
        "Role"
    ])

    users = User.query.order_by(User.id).all()

    for user in users:

        writer.writerow([
            user.id,
            user.name,
            user.email,
            user.role
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=users.csv"
        }
    )

@admin.route("/admin/export/appointments")
@login_required
def export_appointments():
    if current_user.role != "admin":
        abort(403)

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Patient",
        "Doctor",
        "Date",
        "Time",
        "Status"
    ])

    appointments = Appointment.query.all()

    for appointment in appointments:

        writer.writerow([
            appointment.patient.user.name,
            appointment.doctor.user.name,
            appointment.appointment_date,
            appointment.appointment_time,
            appointment.status
        ])

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=appointments.csv"
        }
    )