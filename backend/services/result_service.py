from database import db
from models.result import Result


class ResultService:

    @staticmethod
    def create_result(
        student,
        exam,
        processing_job=None
    ):

        existing = Result.query.filter_by(
            student_id=student.id,
            exam_id=exam.id
        ).first()

        if existing:
            return existing

        result = Result(
            student_id=student.id,
            exam_id=exam.id,
            processing_job_id=processing_job.id if processing_job else None,
            overall_result="PASS",
            sgpa=0.0,
            cgpa=student.cgpa
        )

        db.session.add(result)
        db.session.commit()

        return result