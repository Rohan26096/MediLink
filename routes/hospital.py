from flask import Blueprint, render_template
from flask_login import login_required

hospital = Blueprint("hospital", __name__)


@hospital.route("/hospital/dashboard")
@login_required
def dashboard():
    return render_template("hospital/dashboard.html")