from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    FloatField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired


class DoctorEditProfileForm(FlaskForm):

    specialization = StringField(
        "Specialization",
        validators=[DataRequired()]
    )

    qualification = StringField(
        "Qualification",
        validators=[DataRequired()]
    )

    experience = IntegerField(
        "Experience (Years)",
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

    submit = SubmitField("Update Profile")