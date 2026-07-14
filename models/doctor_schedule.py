from models import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    hospital_id = db.Column(
        db.Integer,
        db.ForeignKey("hospitals.id"),
        nullable=False
    )

    appointments = db.relationship(
        "Appointment",
        backref="doctor",
        lazy=True
    )

    schedules = db.relationship(
        "DoctorSchedule",
        back_populates="doctor",
        cascade="all, delete-orphan"
    )

    specialization = db.Column(
        db.String(100),
        nullable=False
    )

    qualification = db.Column(
        db.String(150),
        nullable=False
    )

    experience = db.Column(
        db.Integer,
        nullable=False
    )

    department = db.Column(
        db.String(100),
        nullable=False
    )

    consultation_fee = db.Column(
        db.Float,
        nullable=False
    )

    bio = db.Column(db.Text)