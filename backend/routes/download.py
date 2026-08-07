from flask import Blueprint, send_from_directory
from pathlib import Path

download_bp = Blueprint("download", __name__)

@download_bp.route("/<path:filename>")
def download(filename):

    output_dir = Path("outputs").resolve()

    return send_from_directory(
        output_dir,
        Path(filename).name,
        as_attachment=True
    )