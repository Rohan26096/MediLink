from flask_mail import Message

mail = None


def send_email(recipient, subject, body):

    msg = Message(
        subject,
        recipients=[recipient]
    )

    msg.body = body

    mail.send(msg)
