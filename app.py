from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db
from models.user import User
from routes.auth import auth


app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(auth)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


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