import os


class FileValidationService:

    ALLOWED_PDF = {".pdf"}
    ALLOWED_EXCEL = {".xlsx"}

    @staticmethod
    def validate(pdf, excel):

        errors = []

        # PDF validation
        if pdf.filename == "":
            errors.append("No PDF file selected.")

        elif not pdf.filename.lower().endswith(".pdf"):
            errors.append("Only PDF files are allowed.")

        # Excel validation
        if excel.filename == "":
            errors.append("No Excel file selected.")

        elif not excel.filename.lower().endswith(".xlsx"):
            errors.append("Only .xlsx Excel files are allowed.")

        return {
            "success": len(errors) == 0,
            "errors": errors
        }