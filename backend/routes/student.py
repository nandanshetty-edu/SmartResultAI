from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.student_service import StudentService


student_bp = Blueprint(
    "student",
    __name__
)


# ============================================================
# STUDENT PROFILE
# ============================================================

@student_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)

        profile = StudentService.get_profile(
            user_id
        )

        if profile is None:
            return jsonify({
                "success": False,
                "message": "Student profile not found"
            }), 404

        return jsonify({
            "success": True,
            "student": profile
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Failed to fetch student profile",
            "error": str(e)
        }), 500


# ============================================================
# ALL PUBLISHED RESULTS
# ============================================================

@student_bp.route("/results", methods=["GET"])
@jwt_required()
def get_results():

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)

        results = StudentService.get_results(
            user_id
        )

        if results is None:
            return jsonify({
                "success": False,
                "message": "Student profile not found"
            }), 404

        return jsonify({
            "success": True,
            "results": results
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Failed to fetch results",
            "error": str(e)
        }), 500


# ============================================================
# SINGLE RESULT
# ============================================================

@student_bp.route(
    "/results/<int:result_id>",
    methods=["GET"]
)
@jwt_required()
def get_result(result_id):

    user_id = get_jwt_identity()

    try:
        user_id = int(user_id)

        result = StudentService.get_result(
            user_id=user_id,
            result_id=result_id
        )

        if result is None:
            return jsonify({
                "success": False,
                "message": "Result not found"
            }), 404

        return jsonify({
            "success": True,
            "result": result
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": "Failed to fetch result",
            "error": str(e)
        }), 500