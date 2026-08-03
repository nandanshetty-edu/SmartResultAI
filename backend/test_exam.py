from app import app
from services.exam_service import ExamService

with app.app_context():

    exam = ExamService.get_or_create(
        academic_year="2025-26",
        semester=2,
        section="A",
        exam_type="Regular",
        exam_month="July",
        exam_year=2026,
        department_id=1,
        created_by=1,
    )

    print("=" * 50)
    print("Exam Created / Retrieved")
    print("=" * 50)
    print("ID :", exam.id)
    print("Academic Year :", exam.academic_year)
    print("Semester :", exam.semester)
    print("Exam Type :", exam.exam_type)
