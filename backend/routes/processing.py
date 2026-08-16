from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from models.exam import Exam
from models.teacher import Teacher

from services.processing_service import ProcessingService
from services.excel_service import ExcelService
from services.file_validation_service import FileValidationService
from services.cleanup_service import CleanupService


processing_bp = Blueprint(
    "processing",
    __name__
)


# ============================================================
# PROCESS RESULT
# TEACHER ONLY
# ============================================================

@processing_bp.route(
    "/process",
    methods=["POST"]
)
@jwt_required()
def process():

    try:

        # ======================================================
        # CHECK USER ROLE
        # ======================================================

        claims = get_jwt()

        role = claims.get("role")

        if role != "TEACHER":

            return jsonify({
                "success": False,
                "message": "Only teachers can process results."
            }), 403

        # ======================================================
        # GET CURRENT USER
        # ======================================================

        user_id = get_jwt_identity()

        teacher = Teacher.query.filter_by(
            user_id=int(user_id)
        ).first()

        if teacher is None:

            return jsonify({
                "success": False,
                "message": "Teacher profile not found."
            }), 404

        # ======================================================
        # CHECK UPLOADED FILES
        # ======================================================

        if "pdf" not in request.files:

            return jsonify({
                "success": False,
                "message": "PDF file is required."
            }), 400

        if "excel" not in request.files:

            return jsonify({
                "success": False,
                "message": "Excel file is required."
            }), 400

        pdf = request.files["pdf"]

        excel = request.files["excel"]

        # ======================================================
        # VALIDATE FILE TYPES
        # ======================================================

        validation = FileValidationService.validate(
            pdf,
            excel
        )

        if not validation["success"]:

            return jsonify({
                "success": False,
                "errors": validation["errors"]
            }), 400

        # ======================================================
        # GET EXAM ID
        # ======================================================

        exam_id = request.form.get(
            "exam_id"
        )

        if not exam_id:

            return jsonify({
                "success": False,
                "message": "exam_id is required."
            }), 400

        # ======================================================
        # FIND EXAM
        # ======================================================

        try:

            exam_id = int(exam_id)

        except ValueError:

            return jsonify({
                "success": False,
                "message": "Invalid exam_id."
            }), 400

        exam = Exam.query.get(
            exam_id
        )

        if exam is None:

            return jsonify({
                "success": False,
                "message": "Exam not found."
            }), 404

        # ======================================================
        # TEACHER DEPARTMENT SECURITY
        # ======================================================

        if (
            teacher.department_id is not None
            and exam.department_id != teacher.department_id
        ):

            return jsonify({
                "success": False,
                "message": (
                    "You are not authorized to process "
                    "results for this department."
                )
            }), 403

        # ======================================================
        # SAVE UPLOADED FILES
        # ======================================================

        uploaded = ProcessingService.upload(
            pdf,
            excel
        )

        # ======================================================
        # PROCESS RESULT
        # ======================================================

        summary = ProcessingService.process(
            uploaded["pdf_path"],
            uploaded["excel_path"],
            exam
        )

        # ======================================================
        # PROCESSING FAILED
        # ======================================================

        if not summary["success"]:

            CleanupService.cleanup(
                uploaded["pdf_path"],
                uploaded["excel_path"]
            )

            return jsonify(
                summary
            ), 400

        # ======================================================
        # GENERATE OUTPUT EXCEL
        # ======================================================

        output_file = ExcelService.generate(
            uploaded["excel_path"],
            exam
        )

        filename = output_file.split("/")[-1]

        # ======================================================
        # CLEANUP INPUT FILES
        # ======================================================

        CleanupService.cleanup(
            uploaded["pdf_path"],
            uploaded["excel_path"]
        )

        # ======================================================
        # SUCCESS
        # ======================================================

        return jsonify({

            "success": True,

            "message":
                "Processing completed successfully.",

            "summary": {

                "students":
                    summary["students"],

                "results":
                    summary["results"],

                "marks":
                    summary["marks"]

            },

            "filename":
                filename,

            "download_url":
                f"/api/download/{filename}"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500