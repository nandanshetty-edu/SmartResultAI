from flask import Blueprint, request, jsonify

from services.processing_service import ProcessingService

processing_bp = Blueprint("processing", __name__)


@processing_bp.route("/upload", methods=["POST"])
def upload():

    if "pdf" not in request.files:

        return jsonify({"success": False, "message": "PDF missing"}), 400

    if "excel" not in request.files:

        return jsonify({"success": False, "message": "Excel missing"}), 400

    pdf = request.files["pdf"]

    excel = request.files["excel"]

    result = ProcessingService.upload(pdf, excel)

    return jsonify({"success": True, "data": result})
