from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from routes.auth import auth

from routes.patient import patient
from routes.doctor import doctor
from routes.hospital import hospital
from routes.admin import admin
from routes.medical_records import medical_records


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(doctor)
app.register_blueprint(hospital)
app.register_blueprint(admin)
app.register_blueprint(medical_records)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)