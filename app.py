from flask import Flask, render_template
from flask_login import LoginManager
from flask_mail import Mail

from config import Config
from models import db
from models.user import User

from routes.auth import auth
from routes.patient import patient
from routes.doctor import doctor
from routes.hospital import hospital
from routes.admin import admin
from routes.medical_records import medical_records
from routes.notification import notification

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)

mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(doctor)
app.register_blueprint(hospital)
app.register_blueprint(admin)
app.register_blueprint(medical_records)
app.register_blueprint(notification)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")

import utils.email
utils.email.mail = mail

with app.app_context():

    admin = User.query.filter_by(
        email="hospital@medilink.com"
    ).first()

    if not admin:

        admin = User(
            name="City Hospital",
            email="hospital@medilink.com",
            role="hospital_admin"
        )

        admin.set_password("123456")

        db.session.add(admin)
        db.session.commit()

        print("Hospital Admin Created")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(500)
def server_error(error):
    db.session.rollback()
    return render_template("errors/500.html"), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)