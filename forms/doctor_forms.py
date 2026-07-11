from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    PasswordField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


class DoctorProfileForm(FlaskForm):

    name = StringField(
        "Doctor Name",
        validators=[DataRequired()]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Temporary Password",
        validators=[
            DataRequired(),
            Length(min=8)
        ]
    )

    specialization = StringField(
        "Specialization",
        validators=[DataRequired()]
    )

    qualification = StringField(
        "Qualification",
        validators=[DataRequired()]
    )

    experience = IntegerField(
        "Experience",
        validators=[DataRequired()]
    )

    department = StringField(
        "Department",
        validators=[DataRequired()]
    )

    consultation_fee = FloatField(
        "Consultation Fee",
        validators=[DataRequired()]
    )

    bio = TextAreaField("Professional Bio")

    submit = SubmitField("Create Doctor")