from flask import Blueprint, request, jsonify

from models.exam import Exam

from services.processing_service import ProcessingService
from services.excel_service import ExcelService
from services.file_validation_service import FileValidationService
from services.cleanup_service import CleanupService

processing_bp = Blueprint(
    "processing",
    __name__
)


@processing_bp.route("/process", methods=["POST"])
def process():

    try:

        # ----------------------------
        # Check Uploaded Files
        # ----------------------------

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

        # ----------------------------
        # Validate File Types
        # ----------------------------

        validation = FileValidationService.validate(
            pdf,
            excel
        )

        if not validation["success"]:
            return jsonify({
                "success": False,
                "errors": validation["errors"]
            }), 400

        # ----------------------------
        # Validate Exam
        # ----------------------------

        exam_id = request.form.get("exam_id")

        if not exam_id:
            return jsonify({
                "success": False,
                "message": "exam_id is required."
            }), 400

        exam = Exam.query.get(exam_id)

        if not exam:
            return jsonify({
                "success": False,
                "message": "Exam not found."
            }), 404

        # ----------------------------
        # Save Uploaded Files
        # ----------------------------

        uploaded = ProcessingService.upload(
            pdf,
            excel
        )

        # ----------------------------
        # Process PDF
        # ----------------------------

        summary = ProcessingService.process(
            uploaded["pdf_path"],
            uploaded["excel_path"],
            exam
        )

        if not summary["success"]:

            CleanupService.cleanup(
                uploaded["pdf_path"],
                uploaded["excel_path"]
            )

            return jsonify(summary), 400

        # ----------------------------
        # Generate Excel
        # ----------------------------

        output_file = ExcelService.generate(
            uploaded["excel_path"],
            exam
        )

        filename = output_file.split("/")[-1]

        # ----------------------------
        # Cleanup Uploaded Files
        # ----------------------------

        CleanupService.cleanup(
            uploaded["pdf_path"],
            uploaded["excel_path"]
        )

        # ----------------------------
        # Success Response
        # ----------------------------

        return jsonify({

            "success": True,

            "message": "Processing completed successfully.",

            "summary": {
                "students": summary["students"],
                "results": summary["results"],
                "marks": summary["marks"]
            },

            "filename": filename,

            "download_url": f"/api/download/{filename}"

        }), 200

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500