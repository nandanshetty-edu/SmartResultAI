from pathlib import Path


class CleanupService:

    @staticmethod
    def delete_file(path):

        file = Path(path)

        if file.exists():
            file.unlink()

    @staticmethod
    def cleanup(pdf_path, excel_path):

        CleanupService.delete_file(pdf_path)
        CleanupService.delete_file(excel_path)