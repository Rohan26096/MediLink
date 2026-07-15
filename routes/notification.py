from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for
)

from flask_login import (
    login_required,
    current_user
)

from models.notification import Notification
from models import db
from flask import flash

notification = Blueprint(
    "notification",
    __name__
)


@notification.route("/notifications")
@login_required
def notifications():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@notification.route("/notifications/read/<int:id>")
@login_required
def mark_read(id):

    notification = Notification.query.get_or_404(id)

    if notification.user_id != current_user.id:
        return redirect(
            url_for("notification.notifications")
        )

    notification.is_read = True

    db.session.commit()

    flash(
        "Notification marked as read.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )


@notification.route("/notifications/delete/<int:id>")
@login_required
def delete_notification(id):

    notification = Notification.query.get_or_404(id)

    if notification.user_id != current_user.id:
        return redirect(
            url_for("notification.notifications")
        )

    db.session.delete(notification)

    db.session.commit()

    flash(
        "Notification deleted.",
        "success"
    )

    return redirect(
        url_for("notification.notifications")
    )