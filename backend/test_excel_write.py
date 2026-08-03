from pathlib import Path

from app import app

from models.exam import Exam

from services.excel_service import ExcelService


excel_path = list(
    Path("sample_data/excel").glob("*.xlsx")
)[0]


with app.app_context():

    workbook, sheet = ExcelService.load_template(
        excel_path
    )

    subject_map = ExcelService.build_subject_map(
        sheet
    )

    exam = Exam.query.first()

    ExcelService.write_student_marks(
        sheet,
        12,
        exam,
        subject_map
    )

    print("Done")