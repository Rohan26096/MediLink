import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-this-secret-key"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "database", "medilink.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "rohan.muni.24@gmail.com"    
    MAIL_PASSWORD = "ymxrorkehbsomgiq"
    MAIL_DEFAULT_SENDER = ("MediLink", MAIL_USERNAME)