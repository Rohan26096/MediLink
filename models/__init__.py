from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.user import User
from models.patient import Patient
from models.medical_record import MedicalRecord
from .doctor import Doctor
from .hospital import Hospital