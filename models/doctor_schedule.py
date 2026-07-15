from models import db


class DoctorSchedule(db.Model):

    __tablename__ = "doctor_schedules"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(
        db.Integer,
        db.ForeignKey("doctors.id"),
        nullable=False
    )

    day = db.Column(db.String(20), nullable=False)

    start_time = db.Column(db.Time, nullable=False)

    end_time = db.Column(db.Time, nullable=False)

    is_available = db.Column(
        db.Boolean,
        default=True
    )

    doctor = db.relationship(
        "Doctor",
        back_populates="schedules"
    )