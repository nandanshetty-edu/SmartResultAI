import os
import uuid
from werkzeug.utils import secure_filename


class FileUtils:

    @staticmethod
    def save_file(file, folder):

        os.makedirs(folder, exist_ok=True)

        extension = os.path.splitext(
            secure_filename(file.filename)
        )[1]

        filename = f"{uuid.uuid4().hex}{extension}"

        filepath = os.path.join(folder, filename)

        file.save(filepath)

        return filepath