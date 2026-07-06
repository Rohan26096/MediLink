from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


class HospitalProfileForm(FlaskForm):

    name = StringField(
        "Hospital Name",
        validators=[
            DataRequired(),
            Length(max=150)
        ]
    )

    email = StringField(
        "Hospital Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(max=20)
        ]
    )

    address = TextAreaField(
        "Address",
        validators=[DataRequired()]
    )

    description = TextAreaField(
        "Hospital Description"
    )

    submit = SubmitField("Save Profile")