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

from models import db
from models.notification import Notification

notification = Blueprint(
    "notification",
    __name__
)


@notification.route("/notifications")
@login_required
def index():

    notifications = (
        Notification.query
        .filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return render_template(
        "notification/index.html",
        notifications=notifications
    )


@notification.route("/notifications/read/<int:id>")
@login_required
def read(id):

    notification = Notification.query.get_or_404(id)

    if notification.user_id != current_user.id:

        return redirect(
            url_for("notification.index")
        )

    notification.is_read = True

    db.session.commit()

    return redirect(
        url_for("notification.index")
    )


@notification.route("/notifications/read-all")
@login_required
def read_all():

    Notification.query.filter_by(
        user_id=current_user.id,
        is_read=False
    ).update(
        {
            "is_read": True
        }
    )

    db.session.commit()

    return redirect(
        url_for("notification.index")
    )