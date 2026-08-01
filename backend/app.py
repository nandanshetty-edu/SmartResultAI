from flask import Flask, jsonify

from flask_cors import CORS

from config import Config

from database import db

from models import *

from routes.auth import auth_bp

from flask_jwt_extended import JWTManager


app = Flask(__name__)

app.config.from_object(Config)

jwt = JWTManager(app)

CORS(app)

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")


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