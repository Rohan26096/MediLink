from flask import redirect, url_for
from flask import request
from flask import (
    Blueprint,
    render_template,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.hospital import Hospital
from forms.doctor_forms import DoctorProfileForm
from models.user import User
from models.doctor import Doctor
from forms.hospital_forms import HospitalProfileForm
from models.doctor import Doctor
from models.patient import Patient
from models.appointment import Appointment


hospital = Blueprint("hospital", __name__)


@hospital.route("/hospital/dashboard")
@login_required
def dashboard():

    hospital = Hospital.query.filter_by(
        admin_id=current_user.id
    ).first()

    if not hospital:

        flash(
            "Please complete your hospital profile first.",
            "warning"
        )

        return redirect(
            url_for("hospital.profile")
        )

    doctor_count = Doctor.query.filter_by(
        hospital_id=hospital.id
    ).count()

    appointment_count = Appointment.query.filter_by(
        hospital_id=hospital.id
    ).count()

    patient_count = (
        db.session.query(Appointment.patient_id)
        .filter_by(hospital_id=hospital.id)
        .distinct()
        .count()
    )

    pending = Appointment.query.filter_by(
        hospital_id=hospital.id,
        status="Pending"
    ).count()

    completed = Appointment.query.filter_by(
        hospital_id=hospital.id,
        status="Completed"
    ).count()

    return render_template(
        "hospital/dashboard.html",
        doctor_count=doctor_count,
        appointment_count=appointment_count,
        patient_count=patient_count,
        pending=pending,
        completed=completed
    )

@hospital.route(
    "/hospital/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    form = HospitalProfileForm()

    hospital = Hospital.query.first()

    if not hospital:

        hospital = Hospital(
            admin_id=current_user.id
        )

    if form.validate_on_submit():

        hospital.admin_id = current_user.id
        hospital.name = form.name.data
        hospital.email = form.email.data
        hospital.phone = form.phone.data
        hospital.address = form.address.data
        hospital.description = form.description.data

        db.session.add(hospital)
        db.session.commit()

        flash(
            "Hospital profile updated successfully!",
            "success"
        )

        return redirect(url_for("hospital.profile"))

    elif hospital.id:

        form.name.data = hospital.name
        form.email.data = hospital.email
        form.phone.data = hospital.phone
        form.address.data = hospital.address
        form.description.data = hospital.description

    return render_template(
        "hospital/profile.html",
        form=form
    )

@hospital.route("/hospital/doctors")
@login_required
def doctors():

    hospital = Hospital.query.first()

    doctors = Doctor.query.filter_by(
        hospital_id=hospital.id
    ).all()

    return render_template(
        "hospital/doctors.html",
        doctors=doctors
    )

@hospital.route("/hospital/analytics")
@login_required
def analytics():
    return render_template("hospital/analytics.html")

@hospital.route(
    "/hospital/doctors/add",
    methods=["GET", "POST"]
)
@login_required
def add_doctor():

    form = DoctorProfileForm()

    if form.validate_on_submit():

        # Check if email already exists
        existing_user = User.query.filter_by(
            email=form.email.data
        ).first()

        if existing_user:
            flash("Email already exists.", "danger")
            return render_template(
                "hospital/add_doctor.html",
                form=form
            )

        hospital = Hospital.query.filter_by(
            admin_id=current_user.id
        ).first()

        # Create User
        user = User(
            name=form.name.data,
            email=form.email.data,
            role="doctor"
        )

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.flush()

        # Create Doctor Profile
        doctor = Doctor(
            user_id=user.id,
            hospital_id=hospital.id,
            specialization=form.specialization.data,
            qualification=form.qualification.data,
            experience=form.experience.data,
            department=form.department.data,
            consultation_fee=form.consultation_fee.data,
            bio=form.bio.data
        )

        db.session.add(doctor)
        db.session.commit()

        flash(
            "Doctor created successfully!",
            "success"
        )

        return redirect(
            url_for("hospital.doctors")
        )

    return render_template(
        "hospital/add_doctor.html",
        form=form
    )
@hospital.route(
    "/hospital/doctors/edit/<int:doctor_id>",
    methods=["GET", "POST"]
)
@login_required
def edit_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)

    user = User.query.get(doctor.user_id)

    form = DoctorProfileForm()

    if form.validate_on_submit():

        user.name = form.name.data
        user.email = form.email.data

        doctor.specialization = form.specialization.data
        doctor.qualification = form.qualification.data
        doctor.experience = form.experience.data
        doctor.department = form.department.data
        doctor.consultation_fee = form.consultation_fee.data
        doctor.bio = form.bio.data

        db.session.commit()

        flash(
            "Doctor updated successfully!",
            "success"
        )

        return redirect(
            url_for("hospital.doctors")
        )

    elif request.method == "GET":

        form.name.data = user.name
        form.email.data = user.email

        form.specialization.data = doctor.specialization
        form.qualification.data = doctor.qualification
        form.experience.data = doctor.experience
        form.department.data = doctor.department
        form.consultation_fee.data = doctor.consultation_fee
        form.bio.data = doctor.bio

    return render_template(
        "hospital/edit_doctor.html",
        form=form
    )

@hospital.route("/hospital/doctors/delete/<int:doctor_id>")
@login_required
def delete_doctor(doctor_id):

    doctor = Doctor.query.get_or_404(doctor_id)

    user = User.query.get_or_404(
        doctor.user_id
    )

    db.session.delete(doctor)
    db.session.delete(user)

    db.session.commit()

    flash(
        "Doctor deleted successfully!",
        "success"
    )

    return redirect(
        url_for("hospital.doctors")
    )

@hospital.route("/hospital/appointments")
@login_required
def appointments():

    hospital = Hospital.query.first()

    status = request.args.get("status")

    status = request.args.get("status")
    search = request.args.get("search", "").strip()

    appointments = Appointment.query.filter_by(
        hospital_id=hospital.id
    )

    if status:
        appointments = appointments.filter_by(status=status)

    if search:
        appointments = (
            appointments
            .join(Doctor)
            .join(User)
            .filter(User.name.ilike(f"%{search}%"))
        )
    page = request.args.get("page", 1, type=int)
    per_page = 10

    appointments = appointments.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    if status:
        appointments = appointments.filter_by(status=status)

    appointments = appointments.order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template(
        "hospital/appointments.html",
        appointments=appointments
    )