from database import db

from utils.file_utils import FileUtils

from services.student_service import StudentService
from services.result_service import ResultService
from services.subject_service import SubjectService
from services.mark_service import MarkService
from services.validation_service import ValidationService
from services.gpa_service import GPAService


class ProcessingService:

    # ============================================================
    # UPLOAD FILES
    # ============================================================

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

    # ============================================================
    # PROCESS RESULT
    # ============================================================

    @staticmethod
    def process(
        pdf_path,
        excel_path,
        exam
    ):

        # --------------------------------------------------------
        # Validate PDF + Excel
        # --------------------------------------------------------

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

            # ====================================================
            # PROCESS EVERY STUDENT
            # ====================================================

            for parsed_student in parsed_students:

                # ------------------------------------------------
                # STUDENT
                # ------------------------------------------------

                student = StudentService.get_or_create(
                    parsed_student,
                    exam
                )

                saved_students += 1

                # ------------------------------------------------
                # RESULT
                # ------------------------------------------------

                result = ResultService.create_result(
                    student=student,
                    exam=exam,
                    overall_result=(
                        parsed_student.overall_result
                    )
                )

                created_results += 1

                # ------------------------------------------------
                # MARKS
                # ------------------------------------------------

                for parsed_subject in (
                    parsed_student.subjects.values()
                ):

                    subject = SubjectService.get_or_create(
                        subject_code=(
                            parsed_subject.subject_code
                        ),
                        semester=exam.semester,
                        department_id=(
                            exam.department_id
                        )
                    )

                    MarkService.create_mark(
                        result=result,
                        subject=subject,
                        parsed_subject=parsed_subject
                    )

                    created_marks += 1

                # ------------------------------------------------
                # CALCULATE CURRENT SGPA
                #
                # All marks for this result have now been
                # inserted/flushed.
                # ------------------------------------------------

                result.sgpa = (
                    GPAService.calculate_sgpa(
                        result
                    )
                )

                # ------------------------------------------------
                # Flush so the current result is visible to the
                # CGPA query within this transaction.
                # ------------------------------------------------

                db.session.flush()

                # ------------------------------------------------
                # Calculate cumulative CGPA
                # ------------------------------------------------

                result.cgpa = (
                    GPAService.calculate_cgpa(
                        student
                    )
                )

                student.cgpa = result.cgpa

                db.session.flush()

            # ====================================================
            # COMMIT ENTIRE PROCESSING JOB ONCE
            # ====================================================

            db.session.commit()

            return {
                "success": True,
                "students": saved_students,
                "results": created_results,
                "marks": created_marks
            }

        except Exception as e:

            # ====================================================
            # ROLLBACK EVERYTHING
            # ====================================================

            db.session.rollback()

            return {
                "success": False,
                "errors": [
                    str(e)
                ]
            }