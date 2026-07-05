from datetime import datetime
from models import db


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=False
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    record_type = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text
    )

    file_name = db.Column(
        db.String(255)
    )

    uploaded_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )