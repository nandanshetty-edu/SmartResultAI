from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from database import db

from models import *

from routes.auth import auth_bp
from routes.processing import processing_bp
from routes.exam import exam_bp
from routes.download import download_bp

app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

CORS(app)

db.init_app(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(processing_bp, url_prefix="/api/processing")
app.register_blueprint(exam_bp, url_prefix="/api/exams")
app.register_blueprint(download_bp, url_prefix="/api/download")

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return jsonify({
        "project": "SmartResult AI",
        "version": "1.0"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "SmartResult AI Backend Running"
    })


if __name__ == "__main__":
    app.run(debug=True)