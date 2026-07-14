from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    TimeField,
    BooleanField,
    SubmitField
)
from wtforms.validators import DataRequired


class DoctorScheduleForm(FlaskForm):

    day = SelectField(
        "Day",
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
            ("Saturday", "Saturday"),
            ("Sunday", "Sunday")
        ],
        validators=[DataRequired()]
    )

    start_time = TimeField(
        "Start Time",
        validators=[DataRequired()]
    )

    end_time = TimeField(
        "End Time",
        validators=[DataRequired()]
    )

    is_available = BooleanField(
        "Available",
        default=True
    )

    submit = SubmitField("Save Schedule")