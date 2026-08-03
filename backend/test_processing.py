from app import app

from models.exam import Exam
from services.processing_service import ProcessingService


with app.app_context():

    exam = Exam.query.first()

    print("=" * 50)
    print("Exam Object:", exam)
    print("Exam ID:", exam.id if exam else None)
    print("=" * 50)

    summary = ProcessingService.process(
        "sample_data/pdf/Poornima_merged.pdf",
        exam
    )

    print()
    print("=" * 50)
    print(summary)
    print("=" * 50)