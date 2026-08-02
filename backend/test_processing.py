from app import app

from models.exam import Exam

from services.processing_service import ProcessingService


with app.app_context():

    exam = Exam.query.first()

    summary = ProcessingService.process(

        "sample_data/pdf/Poornima_merged.pdf",

        exam

    )

    print()

    print("=" * 50)

    print(summary)

    print("=" * 50)