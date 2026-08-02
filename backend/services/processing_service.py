from utils.file_utils import FileUtils


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