from collections import Counter

from services.parser.camelot_parser import CamelotParser
from services.excel_service import ExcelService


class ValidationService:

    @staticmethod
    def validate(pdf_path, excel_path):

        errors = []

        # -----------------------------
        # Parse PDF
        # -----------------------------

        parsed_students = CamelotParser.parse(pdf_path)

        if len(parsed_students) == 0:

            errors.append(
                "No students found in uploaded PDF."
            )

            return {
                "success": False,
                "errors": errors
            }

        # -----------------------------
        # Load Excel
        # -----------------------------

        workbook, sheet = ExcelService.load_template(
            excel_path
        )

        subject_map = ExcelService.build_subject_map(
            sheet
        )

        if len(subject_map) == 0:

            errors.append(
                "No subject codes found in Excel template."
            )

        # -----------------------------
        # Subject Validation
        # -----------------------------

        pdf_subjects = set()

        for student in parsed_students:

            pdf_subjects.update(
                student.subjects.keys()
            )

        excel_subjects = set(
            subject_map.keys()
        )

        missing_in_excel = sorted(
            pdf_subjects - excel_subjects
        )

        extra_in_excel = sorted(
            excel_subjects - pdf_subjects
        )

        if missing_in_excel:

            errors.append(
                "Missing subjects in Excel: "
                + ", ".join(missing_in_excel)
            )

        if extra_in_excel:

            errors.append(
                "Unexpected subjects in Excel: "
                + ", ".join(extra_in_excel)
            )

        # -----------------------------
        # Duplicate USN Validation
        # -----------------------------

        usns = [
            student.usn
            for student in parsed_students
        ]

        duplicate_usns = [

            usn

            for usn, count in Counter(usns).items()

            if count > 1

        ]

        if duplicate_usns:

            errors.append(
                "Duplicate USNs found in PDF: "
                + ", ".join(duplicate_usns)
            )

        # -----------------------------
        # Result
        # -----------------------------

        if errors:

            return {

                "success": False,

                "errors": errors

            }

        return {

            "success": True,

            "students": parsed_students

        }