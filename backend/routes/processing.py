from flask import Blueprint, request, jsonify

processing_bp = Blueprint("processing", __name__)


@processing_bp.route("/upload", methods=["POST"])
def upload_files():

    if "pdf" not in request.files:
        return jsonify({
            "success": False,
            "message": "PDF not uploaded"
        }), 400

    if "excel" not in request.files:
        return jsonify({
            "success": False,
            "message": "Excel not uploaded"
        }), 400

    pdf = request.files["pdf"]
    excel = request.files["excel"]

    return jsonify({

        "success": True,

        "pdf": pdf.filename,

        "excel": excel.filename

    })