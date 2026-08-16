from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import db

from models.user import User

from services.auth_service import AuthService
from utils.jwt_utils import generate_token


auth_bp = Blueprint("auth", __name__)


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email:
        return jsonify({
            "success": False,
            "message": "Email is required"
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password is required"
        }), 400

    if not role:
        return jsonify({
            "success": False,
            "message": "Role is required"
        }), 400

    try:

        user = AuthService.create_user(

            email=email,

            password=password,

            role=role,

            # Teacher fields
            employee_id=data.get("employee_id"),
            designation=data.get("designation"),

            # Common
            name=data.get("name"),
            department_id=data.get("department_id"),

            # Student fields
            usn=data.get("usn"),
            semester=data.get("semester"),
            section=data.get("section"),
        )

        return jsonify({
            "success": True,
            "message": "User created successfully",
            "user": AuthService.serialize_user(user)
        }), 201

    except ValueError as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 400

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": "Failed to create user",
            "error": str(e)
        }), 500


# ============================================================
# LOGIN
# ============================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True) or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:

        return jsonify({
            "success": False,
            "message": "Email and password are required"
        }), 400

    try:

        user = AuthService.authenticate(
            email=email,
            password=password
        )

        token = generate_token(user)

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": AuthService.serialize_user(user)
        }), 200

    except ValueError as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 401

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Login failed",
            "error": str(e)
        }), 500


# ============================================================
# CURRENT USER
# ============================================================

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    user_id = get_jwt_identity()

    try:

        user = AuthService.get_user_by_id(
            int(user_id)
        )

        if user is None:

            return jsonify({
                "success": False,
                "message": "User not found"
            }), 404

        if not user.is_active:

            return jsonify({
                "success": False,
                "message": "Account is inactive"
            }), 403

        return jsonify({
            "success": True,
            "user": AuthService.serialize_user(user)
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Failed to fetch user",
            "error": str(e)
        }), 500