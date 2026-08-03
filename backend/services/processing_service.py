from utils.file_utils import FileUtils

from services.parser.camelot_parser import CamelotParser
from services.student_service import StudentService
from services.result_service import ResultService
from services.subject_service import SubjectService
from services.mark_service import MarkService


class ProcessingService:

    @staticmethod
    def upload(pdf, excel):

        pdf_path = FileUtils.save_file(
            pdf,
            "uploads/pdf"
        )

        excel_path = FileUtils.save_file(
            excel,
            "uploads/excel"
        )

        return {
            "pdf_path": pdf_path,
            "excel_path": excel_path
        }

    @staticmethod
    def process(pdf_path, exam):

        parsed_students = CamelotParser.parse(pdf_path)

        saved_students = 0
        created_results = 0
        created_marks = 0

        for parsed_student in parsed_students:

            student = StudentService.get_or_create(
                parsed_student
            )

            saved_students += 1

            result = ResultService.create_result(
                student,
                exam
            )

            created_results += 1

            for parsed_subject in parsed_student.subjects.values():

                subject = SubjectService.get_or_create(
                    subject_code=parsed_subject.subject_code,
                    semester=exam.semester,
                    department_id=exam.department_id
                )

                MarkService.create_mark(
                    result=result,
                    subject=subject,
                    parsed_subject=parsed_subject
                )

                created_marks += 1

        return {
            "students": saved_students,
            "results": created_results,
            "marks": created_marks
        }