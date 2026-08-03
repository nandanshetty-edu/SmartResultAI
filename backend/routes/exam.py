from flask import Blueprint, request, jsonify

from services.exam_service import ExamService

exam_bp = Blueprint("exam", __name__)


@exam_bp.route("/", methods=["POST"])
def create_exam():

    data = request.get_json()

    required = [
        "academic_year",
        "semester",
        "exam_type",
        "exam_month",
        "exam_year",
        "department_id",
        "created_by",
    ]

    for field in required:

        if field not in data:

            return jsonify({"success": False, "message": f"{field} is required"}), 400

    exam = ExamService.get_or_create(
        academic_year=data["academic_year"],
        semester=data["semester"],
        section=data.get("section"),
        exam_type=data["exam_type"],
        exam_month=data["exam_month"],
        exam_year=data["exam_year"],
        department_id=data["department_id"],
        created_by=data["created_by"],
    )

    return (
        jsonify(
            {
                "success": True,
                "message": "Exam ready",
                "exam": {
                    "id": exam.id,
                    "academic_year": exam.academic_year,
                    "semester": exam.semester,
                    "section": exam.section,
                    "exam_type": exam.exam_type,
                    "exam_month": exam.exam_month,
                    "exam_year": exam.exam_year,
                },
            }
        ),
        201,
    )
