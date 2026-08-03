from flask import Blueprint, request, jsonify
from utils.password_utils import hash_password
from utils.password_utils import verify_password
from utils.jwt_utils import generate_token

from database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password or not role:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    existing = User.query.filter_by(email=email).first()

    if existing:
        return jsonify({"success": False, "message": "Email already exists"}), 400

    user = User(email=email, password=hash_password(password), role=role)

    db.session.add(user)
    db.session.commit()

    return jsonify({"success": True, "message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")

    password = data.get("password")

    if not email or not password:

        return jsonify({"success": False, "message": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()

    if user is None:

        return jsonify({"success": False, "message": "Invalid email"}), 401

    if not verify_password(password, user.password):

        return jsonify({"success": False, "message": "Wrong password"}), 401

    token = generate_token(user)

    return jsonify(
        {"success": True, "token": token, "role": user.role, "email": user.email}
    )
