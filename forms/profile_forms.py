from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    TextAreaField,
    SelectField,
    SubmitField
)
from wtforms.validators import Optional, NumberRange


class PatientProfileForm(FlaskForm):

    age = IntegerField(
        "Age",
        validators=[
            Optional(),
            NumberRange(min=0, max=150)
        ]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("", "Select Gender"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    blood_group = SelectField(
        "Blood Group",
        choices=[
            ("", "Select Blood Group"),
            ("A+", "A+"),
            ("A-", "A-"),
            ("B+", "B+"),
            ("B-", "B-"),
            ("AB+", "AB+"),
            ("AB-", "AB-"),
            ("O+", "O+"),
            ("O-", "O-")
        ]
    )

    phone = StringField("Phone Number")

    address = TextAreaField("Address")

    emergency_contact = StringField("Emergency Contact")

    allergies = TextAreaField("Allergies")

    medical_history = TextAreaField("Medical History")

    submit = SubmitField("Save Profile")