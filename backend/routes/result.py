from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt

from database import db

from models.result import Result
from models.student import Student
from models.exam import Exam
from models.mark import Mark
from models.subject import Subject

from services.result_service import ResultService


result_bp = Blueprint(
    "result",
    __name__
)


# ============================================================
# TEACHER AUTHORIZATION
# ============================================================

def require_teacher():

    claims = get_jwt()

    role = claims.get("role")

    if role != "TEACHER":
        return jsonify({
            "success": False,
            "message": "Only teachers can manage results."
        }), 403

    return None


# ============================================================
# GET ALL RESULTS
#
# Teacher can see all processed results.
# Optional:
#
# GET /api/results
# GET /api/results?exam_id=1
#
# ============================================================

@result_bp.route("/", methods=["GET"])
@jwt_required()
def get_results():

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        exam_id = None

        # --------------------------------------------------------
        # Optional exam filter
        # --------------------------------------------------------

        from flask import request

        exam_id = request.args.get(
            "exam_id",
            type=int
        )

        query = Result.query

        if exam_id is not None:

            query = query.filter_by(
                exam_id=exam_id
            )

        results = query.order_by(
            Result.created_at.desc()
        ).all()

        response = []

        for result in results:

            student = Student.query.get(
                result.student_id
            )

            exam = Exam.query.get(
                result.exam_id
            )

            response.append({

                "id": result.id,

                "student": {

                    "id": (
                        student.id
                        if student
                        else None
                    ),

                    "usn": (
                        student.usn
                        if student
                        else None
                    ),

                    "name": (
                        student.name
                        if student
                        else None
                    ),

                    "semester": (
                        student.semester
                        if student
                        else None
                    ),

                    "section": (
                        student.section
                        if student
                        else None
                    ),
                },

                "exam": {

                    "id": (
                        exam.id
                        if exam
                        else None
                    ),

                    "academic_year": (
                        exam.academic_year
                        if exam
                        else None
                    ),

                    "semester": (
                        exam.semester
                        if exam
                        else None
                    ),

                    "section": (
                        exam.section
                        if exam
                        else None
                    ),

                    "exam_type": (
                        exam.exam_type
                        if exam
                        else None
                    ),

                    "exam_month": (
                        exam.exam_month
                        if exam
                        else None
                    ),

                    "exam_year": (
                        exam.exam_year
                        if exam
                        else None
                    ),
                },

                "sgpa": result.sgpa,

                "cgpa": result.cgpa,

                "overall_result":
                    result.overall_result,

                "published":
                    result.published,

                "created_at": (
                    result.created_at.isoformat()
                    if result.created_at
                    else None
                ),
            })

        return jsonify({

            "success": True,

            "count": len(response),

            "results": response

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Failed to fetch results",

            "error": str(e)

        }), 500


# ============================================================
# GET SINGLE RESULT
#
# GET /api/results/1
#
# Includes complete subject-wise marks.
# ============================================================

@result_bp.route(
    "/<int:result_id>",
    methods=["GET"]
)
@jwt_required()
def get_result(result_id):

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        result = ResultService.get_by_id(
            result_id
        )

        if result is None:

            return jsonify({

                "success": False,

                "message":
                    "Result not found"

            }), 404

        student = Student.query.get(
            result.student_id
        )

        exam = Exam.query.get(
            result.exam_id
        )

        marks = Mark.query.filter_by(
            result_id=result.id
        ).all()

        mark_list = []

        for mark in marks:

            subject = Subject.query.get(
                mark.subject_id
            )

            mark_list.append({

                "id": mark.id,

                "subject_id":
                    mark.subject_id,

                "subject_code": (
                    subject.subject_code
                    if subject
                    else None
                ),

                "subject_name": (
                    subject.subject_name
                    if subject
                    else None
                ),

                "credits": (
                    subject.credits
                    if subject
                    else None
                ),

                "internal":
                    mark.internal,

                "external":
                    mark.external,

                "total":
                    mark.total,

                "result":
                    mark.result,
            })

        return jsonify({

            "success": True,

            "result": {

                "id":
                    result.id,

                "student": {

                    "id": (
                        student.id
                        if student
                        else None
                    ),

                    "usn": (
                        student.usn
                        if student
                        else None
                    ),

                    "name": (
                        student.name
                        if student
                        else None
                    ),

                    "semester": (
                        student.semester
                        if student
                        else None
                    ),

                    "section": (
                        student.section
                        if student
                        else None
                    ),
                },

                "exam": {

                    "id": (
                        exam.id
                        if exam
                        else None
                    ),

                    "academic_year": (
                        exam.academic_year
                        if exam
                        else None
                    ),

                    "semester": (
                        exam.semester
                        if exam
                        else None
                    ),

                    "section": (
                        exam.section
                        if exam
                        else None
                    ),

                    "exam_type": (
                        exam.exam_type
                        if exam
                        else None
                    ),

                    "exam_month": (
                        exam.exam_month
                        if exam
                        else None
                    ),

                    "exam_year": (
                        exam.exam_year
                        if exam
                        else None
                    ),
                },

                "sgpa":
                    result.sgpa,

                "cgpa":
                    result.cgpa,

                "overall_result":
                    result.overall_result,

                "published":
                    result.published,

                "marks":
                    mark_list,

                "created_at": (
                    result.created_at.isoformat()
                    if result.created_at
                    else None
                ),
            }

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message":
                "Failed to fetch result",

            "error": str(e)

        }), 500


# ============================================================
# PUBLISH SINGLE RESULT
#
# POST /api/results/1/publish
# ============================================================

@result_bp.route(
    "/<int:result_id>/publish",
    methods=["POST"]
)
@jwt_required()
def publish_result(result_id):

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        result = ResultService.get_by_id(
            result_id
        )

        if result is None:

            return jsonify({

                "success": False,

                "message":
                    "Result not found"

            }), 404

        if result.published:

            return jsonify({

                "success": True,

                "message":
                    "Result is already published",

                "result_id":
                    result.id

            }), 200

        ResultService.publish(
            result
        )

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Result published successfully",

            "result_id":
                result.id,

            "published":
                result.published

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "success": False,

            "message":
                "Failed to publish result",

            "error": str(e)

        }), 500


# ============================================================
# UNPUBLISH SINGLE RESULT
#
# POST /api/results/1/unpublish
# ============================================================

@result_bp.route(
    "/<int:result_id>/unpublish",
    methods=["POST"]
)
@jwt_required()
def unpublish_result(result_id):

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        result = ResultService.get_by_id(
            result_id
        )

        if result is None:

            return jsonify({

                "success": False,

                "message":
                    "Result not found"

            }), 404

        ResultService.unpublish(
            result
        )

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Result unpublished successfully",

            "result_id":
                result.id,

            "published":
                result.published

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "success": False,

            "message":
                "Failed to unpublish result",

            "error": str(e)

        }), 500


# ============================================================
# PUBLISH ALL RESULTS FOR AN EXAM
#
# POST /api/results/exam/1/publish
#
# ============================================================

@result_bp.route(
    "/exam/<int:exam_id>/publish",
    methods=["POST"]
)
@jwt_required()
def publish_exam_results(exam_id):

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        exam = Exam.query.get(
            exam_id
        )

        if exam is None:

            return jsonify({

                "success": False,

                "message":
                    "Exam not found"

            }), 404

        results = Result.query.filter_by(
            exam_id=exam_id
        ).all()

        if not results:

            return jsonify({

                "success": False,

                "message":
                    "No results found for this exam"

            }), 404

        published_count = 0

        for result in results:

            if not result.published:

                ResultService.publish(
                    result
                )

                published_count += 1

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Exam results published successfully",

            "exam_id":
                exam_id,

            "total_results":
                len(results),

            "published_now":
                published_count

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "success": False,

            "message":
                "Failed to publish exam results",

            "error": str(e)

        }), 500


# ============================================================
# UNPUBLISH ALL RESULTS FOR AN EXAM
#
# POST /api/results/exam/1/unpublish
#
# ============================================================

@result_bp.route(
    "/exam/<int:exam_id>/unpublish",
    methods=["POST"]
)
@jwt_required()
def unpublish_exam_results(exam_id):

    unauthorized = require_teacher()

    if unauthorized:
        return unauthorized

    try:

        exam = Exam.query.get(
            exam_id
        )

        if exam is None:

            return jsonify({

                "success": False,

                "message":
                    "Exam not found"

            }), 404

        results = Result.query.filter_by(
            exam_id=exam_id
        ).all()

        if not results:

            return jsonify({

                "success": False,

                "message":
                    "No results found for this exam"

            }), 404

        unpublished_count = 0

        for result in results:

            if result.published:

                ResultService.unpublish(
                    result
                )

                unpublished_count += 1

        db.session.commit()

        return jsonify({

            "success": True,

            "message":
                "Exam results unpublished successfully",

            "exam_id":
                exam_id,

            "total_results":
                len(results),

            "unpublished_now":
                unpublished_count

        }), 200

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "success": False,

            "message":
                "Failed to unpublish exam results",

            "error": str(e)

        }), 500