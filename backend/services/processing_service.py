from utils.file_utils import FileUtils

from services.parser.camelot_parser import CamelotParser
from services.student_service import StudentService
from services.result_service import ResultService


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

        for parsed_student in parsed_students:

            student = StudentService.get_or_create(
                parsed_student
            )

            saved_students += 1

            ResultService.create_result(
                student,
                exam
            )

            created_results += 1

        return {

            "students": saved_students,

            "results": created_results

        }