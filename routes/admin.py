from flask import Blueprint, render_template
from flask_login import login_required

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.hospital import Hospital
from models.appointment import Appointment
from sqlalchemy import or_
from flask import request

admin = Blueprint("admin", __name__)


@admin.route("/admin/dashboard")
@login_required
def dashboard():

    total_users = User.query.count()
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_hospitals = Hospital.query.count()
    total_appointments = Appointment.query.count()

    appointment_status = {
        "Pending": Appointment.query.filter_by(status="Pending").count(),
        "Accepted": Appointment.query.filter_by(status="Accepted").count(),
        "Rejected": Appointment.query.filter_by(status="Rejected").count(),
        "Completed": Appointment.query.filter_by(status="Completed").count()
    }

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_hospitals=total_hospitals,
        total_appointments=total_appointments,
        appointment_status=appointment_status
    )

@admin.route("/admin/users")
@login_required
def users():

    search = request.args.get("search", "")

    users = User.query

    if search:

        users = users.filter(

            or_(

                User.name.ilike(f"%{search}%"),

                User.email.ilike(f"%{search}%"),

                User.role.ilike(f"%{search}%")

            )

        )

    users = users.order_by(User.created_at.desc()).all()

    return render_template(
        "admin/users.html",
        users=users,
        search=search
    )