from datetime import date

from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    DateField,
    TimeField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired, ValidationError


class AppointmentForm(FlaskForm):

    hospital = SelectField(
        "Hospital",
        coerce=int,
        validators=[DataRequired()]
    )

    doctor = SelectField(
        "Doctor",
        coerce=int,
        validators=[DataRequired()]
    )

    appointment_date = DateField(
        "Appointment Date",
        validators=[DataRequired()]
    )

    appointment_time = TimeField(
        "Appointment Time",
        validators=[DataRequired()]
    )

    reason = TextAreaField(
        "Reason for Visit",
        validators=[DataRequired()]
    )

    submit = SubmitField("Book Appointment")

    def validate_appointment_date(self, field):

        if field.data < date.today():
            raise ValidationError(
                "Appointment date cannot be in the past."
            )