from database import db

from utils.file_utils import FileUtils

from services.student_service import StudentService
from services.result_service import ResultService
from services.subject_service import SubjectService
from services.mark_service import MarkService
from services.validation_service import ValidationService


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
    def process(pdf_path, excel_path, exam):

        # --------------------------
        # Validate Uploads
        # --------------------------

        validation = ValidationService.validate(
            pdf_path,
            excel_path
        )

        if not validation["success"]:
            return validation

        parsed_students = validation["students"]

        saved_students = 0
        created_results = 0
        created_marks = 0

        try:

            # --------------------------
            # Save Database
            # --------------------------

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

            # --------------------------
            # Commit Everything
            # --------------------------

            db.session.commit()

            return {

                "success": True,

                "students": saved_students,

                "results": created_results,

                "marks": created_marks

            }

        except Exception as e:

            db.session.rollback()

            return {

                "success": False,

                "errors": [
                    str(e)
                ]

            }