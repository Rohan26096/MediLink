import os

class Config:

    SECRET_KEY = "medilink_secret_key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///instance/medilink.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False