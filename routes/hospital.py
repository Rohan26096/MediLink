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

from forms.hospital_forms import HospitalProfileForm


hospital = Blueprint("hospital", __name__)


@hospital.route("/hospital/dashboard")
@login_required
def dashboard():
    return render_template("hospital/dashboard.html")


@hospital.route(
    "/hospital/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    form = HospitalProfileForm()

    hospital = Hospital.query.first()

    if not hospital:
        hospital = Hospital()

    if form.validate_on_submit():

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