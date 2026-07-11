from flask_mail import Message
from app import mail


def send_email(
    recipient,
    subject,
    body
):

    msg = Message(

        subject,

        recipients=[recipient]

    )

    msg.body = body

    mail.send(msg)