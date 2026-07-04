from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    StringField,
    TextAreaField,
    SelectField,
    SubmitField
)
from wtforms.validators import Optional


class PatientProfileForm(FlaskForm):

    age = IntegerField(
        "Age",
        validators=[Optional()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("", "Select"),
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    blood_group = SelectField(
        "Blood Group",
        choices=[
            ("", "Select"),
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

    phone = StringField("Phone")

    address = TextAreaField("Address")

    emergency_contact = StringField("Emergency Contact")

    allergies = TextAreaField("Allergies")

    medical_history = TextAreaField("Medical History")

    submit = SubmitField("Save Profile")