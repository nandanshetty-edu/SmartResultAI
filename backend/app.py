from flask import Flask, jsonify

from flask_cors import CORS

from config import Config

from database import db

from models import *

from routes.auth import auth_bp

from flask_jwt_extended import JWTManager

from routes.processing import processing_bp

from routes.exam import exam_bp

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(processing_bp, url_prefix="/api/processing")


with app.app_context():
    db.create_all()


@app.route("/")
def home():

    return jsonify({"project": "SmartResult AI", "version": "1.0"})


@app.route("/health")
def health():

    return jsonify({"status": "ok", "message": "SmartResult AI Backend Running"})


app.register_blueprint(exam_bp, url_prefix="/api/exams")

if __name__ == "__main__":

    app.run(debug=True)
