from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired


class PrescriptionForm(FlaskForm):

    medicines = TextAreaField(
        "Medicines",
        validators=[DataRequired()]
    )

    dosage = TextAreaField(
        "Dosage",
        validators=[DataRequired()]
    )

    instructions = TextAreaField(
        "Instructions"
    )

    submit = SubmitField("Save Prescription")