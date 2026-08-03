from pathlib import Path

from app import app
from models.exam import Exam
from services.excel_service import ExcelService


excel_path = list(
    Path("sample_data/excel").glob("*.xlsx")
)[0]


with app.app_context():

    exam = Exam.query.first()

    output = ExcelService.generate(
        excel_path,
        exam
    )

    print()
    print("=" * 50)
    print("Generated Successfully")
    print(output)
    print("=" * 50)