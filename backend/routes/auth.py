from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from database import db

from services.auth_service import AuthService
from utils.jwt_utils import generate_token


auth_bp = Blueprint(
    "auth",
    __name__
)


# ============================================================
# REGISTER
# ============================================================

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(
        silent=True
    ) or {}

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

            # Teacher
            employee_id=data.get(
                "employee_id"
            ),

            designation=data.get(
                "designation"
            ),

            # Common
            name=data.get(
                "name"
            ),

            department_id=data.get(
                "department_id"
            ),

            # Student
            usn=data.get(
                "usn"
            ),

            semester=data.get(
                "semester"
            ),

            section=data.get(
                "section"
            ),
        )

        return jsonify({
            "success": True,
            "message": "User created successfully",
            "user": AuthService.serialize_user(
                user
            )
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
# ACTIVATE IMPORTED STUDENT
#
# Teacher only.
#
# Request:
#
# {
#     "usn": "4MK25CS049",
#     "password": "Student@123"
# }
#
# Student subsequently logs in using:
#
#     USN + password
# ============================================================

@auth_bp.route(
    "/student/activate",
    methods=["POST"]
)
@jwt_required()
def activate_student():

    # --------------------------------------------------------
    # Verify logged-in user is a teacher
    # --------------------------------------------------------

    claims = get_jwt()

    role = (
        claims.get("role") or ""
    ).strip().upper()

    if role != "TEACHER":

        return jsonify({
            "success": False,
            "message": (
                "Only teachers can activate "
                "student accounts"
            )
        }), 403

    # --------------------------------------------------------
    # Request body
    # --------------------------------------------------------

    data = request.get_json(
        silent=True
    ) or {}

    usn = data.get("usn")
    password = data.get("password")

    if not usn:

        return jsonify({
            "success": False,
            "message": "USN is required"
        }), 400

    if not password:

        return jsonify({
            "success": False,
            "message": "Password is required"
        }), 400

    # --------------------------------------------------------
    # Activate student
    # --------------------------------------------------------

    try:

        user = AuthService.activate_student(
            usn=usn,
            password=password
        )

        db.session.commit()

        return jsonify({
            "success": True,
            "message": (
                "Student account activated successfully"
            ),
            "user": AuthService.serialize_user(
                user
            )
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
            "message": "Failed to activate student account",
            "error": str(e)
        }), 500


# ============================================================
# LOGIN
#
# TEACHER:
# {
#     "role": "TEACHER",
#     "email": "...",
#     "password": "..."
# }
#
# STUDENT:
# {
#     "role": "STUDENT",
#     "usn": "...",
#     "password": "..."
# }
# ============================================================

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(
        silent=True
    ) or {}

    role = data.get("role")
    password = data.get("password")

    if not role:
        return jsonify({
            "success": False,
            "message": "Role is required"
        }), 400

    if not password:
        return jsonify({
            "success": False,
            "message": "Password is required"
        }), 400

    role = role.strip().upper()

    try:

        # ========================================================
        # TEACHER LOGIN
        # ========================================================

        if role == "TEACHER":

            email = data.get("email")

            if not email:
                return jsonify({
                    "success": False,
                    "message": "College Gmail is required"
                }), 400

            user = AuthService.authenticate_teacher(
                email=email,
                password=password
            )

        # ========================================================
        # STUDENT LOGIN
        # ========================================================

        elif role == "STUDENT":

            usn = data.get("usn")

            if not usn:
                return jsonify({
                    "success": False,
                    "message": "USN is required"
                }), 400

            user = AuthService.authenticate_student(
                usn=usn,
                password=password
            )

        # ========================================================
        # INVALID ROLE
        # ========================================================

        else:

            return jsonify({
                "success": False,
                "message": "Invalid login role"
            }), 400

        # ========================================================
        # GENERATE JWT
        # ========================================================

        token = generate_token(user)

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": AuthService.serialize_user(
                user
            )
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
            "user": AuthService.serialize_user(
                user
            )
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Failed to fetch user",
            "error": str(e)
        }), 500