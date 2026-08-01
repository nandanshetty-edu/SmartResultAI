import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "smartresult_secret_key"

    JWT_SECRET_KEY = "smartresult_super_secret_key_2026"

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "smartresult.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "smartresult_jwt_secret"

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")