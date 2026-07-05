from models import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        unique=True,
        nullable=False
    )

    age = db.Column(db.Integer)

    gender = db.Column(db.String(20))

    phone = db.Column(db.String(20))

    blood_group = db.Column(db.String(10))

    address = db.Column(db.String(255))

    emergency_contact = db.Column(db.String(20))

    allergies = db.Column(db.Text)

    medical_history = db.Column(db.Text)
    
    medical_records = db.relationship(
    "MedicalRecord",
    backref="patient",
    lazy=True,
    cascade="all, delete-orphan"
)