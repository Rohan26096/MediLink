from datetime import datetime
from models import db


class Prescription(db.Model):
    __tablename__ = "prescriptions"

    id = db.Column(db.Integer, primary_key=True)

    appointment_id = db.Column(
        db.Integer,
        db.ForeignKey("appointments.id"),
        nullable=False
    )

    medicines = db.Column(
        db.Text,
        nullable=False
    )

    dosage = db.Column(
        db.Text,
        nullable=False
    )

    instructions = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )