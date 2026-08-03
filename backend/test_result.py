from app import app

from models.student import Student
from models.exam import Exam

from services.result_service import ResultService

with app.app_context():

    student = Student.query.first()

    exam = Exam.query.first()

    result = ResultService.create_result(student, exam)

    print("=" * 50)

    print("Result Created")

    print("=" * 50)

    print(result.id)

    print(result.student_id)

    print(result.exam_id)

    print(result.overall_result)
