from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import (
    StringField,
    SelectField,
    TextAreaField,
    SubmitField
)

from wtforms.validators import DataRequired


class MedicalRecordForm(FlaskForm):

    title = StringField(
        "Record Title",
        validators=[DataRequired()]
    )

    record_type = SelectField(
        "Record Type",
        choices=[
            ("Lab Report", "Lab Report"),
            ("Prescription", "Prescription"),
            ("X-Ray", "X-Ray"),
            ("MRI", "MRI"),
            ("CT Scan", "CT Scan"),
            ("Blood Test", "Blood Test"),
            ("Other", "Other")
        ]
    )

    description = TextAreaField("Description")

    record_file = FileField(
        "Upload File",
        validators=[
            FileRequired(),
            FileAllowed(
                ["pdf", "png", "jpg", "jpeg"],
                "Only PDF and Image files are allowed."
            )
        ]
    )

    submit = SubmitField("Upload Record")