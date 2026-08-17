from database import db
from models.mark import Mark


class MarkService:

    # ============================================================
    # CREATE / UPDATE MARK
    # ============================================================

    @staticmethod
    def create_mark(
        result,
        subject,
        parsed_subject
    ):

        if result is None:
            raise ValueError(
                "Result is required"
            )

        if subject is None:
            raise ValueError(
                "Subject is required"
            )

        existing = Mark.query.filter_by(
            result_id=result.id,
            subject_id=subject.id
        ).first()

        if existing:

            existing.internal = (
                parsed_subject.internal
            )

            existing.external = (
                parsed_subject.external
            )

            existing.total = (
                parsed_subject.total
            )

            existing.result = (
                parsed_subject.result
            )

            db.session.flush()

            return existing

        mark = Mark(
            result_id=result.id,

            subject_id=subject.id,

            internal=parsed_subject.internal,

            external=parsed_subject.external,

            total=parsed_subject.total,

            result=parsed_subject.result,
        )

        db.session.add(mark)

        db.session.flush()

        return mark

    # ============================================================
    # GET MARKS
    # ============================================================

    @staticmethod
    def get_marks(result_id):

        return Mark.query.filter_by(
            result_id=result_id
        ).all()