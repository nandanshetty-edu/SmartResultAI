from app import app

from services.parser.camelot_parser import CamelotParser
from services.student_service import StudentService


with app.app_context():

    students = CamelotParser.parse(
        "sample_data/pdf/Poornima_merged.pdf"
    )

    saved = 0

    for student in students:

        StudentService.get_or_create(student)

        saved += 1

    print()
    print("=" * 50)
    print(f"Students Parsed : {len(students)}")
    print(f"Students Saved  : {saved}")
    print("=" * 50)