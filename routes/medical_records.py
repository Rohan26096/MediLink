import os
import uuid
from werkzeug.utils import secure_filename
from flask import send_from_directory

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.patient import Patient
from models.medical_record import MedicalRecord

from forms.medical_record_forms import MedicalRecordForm


medical_records = Blueprint(
    "medical_records",
    __name__
)


@medical_records.route(
    "/patient/medical-records",
    methods=["GET", "POST"]
)
@login_required
def records():

    form = MedicalRecordForm()

    patient = Patient.query.filter_by(
        user_id=current_user.id
    ).first()

    if not patient:
        flash("Please complete your profile first.", "warning")
        return redirect(url_for("patient.profile"))

    if form.validate_on_submit():

        file = form.record_file.data

        original_filename = secure_filename(file.filename)

        unique_filename = (
            f"{uuid.uuid4().hex}_{original_filename}"
        )

        upload_folder = os.path.join(
            current_app.root_path,
            "uploads",
            "reports"
        )

        os.makedirs(upload_folder, exist_ok=True)

        filepath = os.path.join(
            upload_folder,
            unique_filename
        )

        file.save(filepath)

        record = MedicalRecord(
            patient_id=patient.id,
            title=form.title.data,
            record_type=form.record_type.data,
            description=form.description.data,
            file_name=unique_filename
        )

        db.session.add(record)
        db.session.commit()

        flash("Medical record uploaded successfully!", "success")

        return redirect(
            url_for("medical_records.records")
        )

    records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).all()

    return render_template(
        "patient/medical_records.html",
        form=form,
        records=records
    )


@medical_records.route("/patient/medical-records/download/<filename>")
@login_required
def download_record(filename):

    upload_folder = os.path.join(
        current_app.root_path,
        "uploads",
        "reports"
    )

    return send_from_directory(
        upload_folder,
        filename,
        as_attachment=True
    )