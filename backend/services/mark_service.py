from database import db
from models.mark import Mark


class MarkService:

    @staticmethod
    def create_mark(result, subject, parsed_subject):

        existing = Mark.query.filter_by(
            result_id=result.id, subject_id=subject.id
        ).first()

        if existing:
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
        db.session.commit()

        return mark

    @staticmethod
    def get_marks(result_id):

        return Mark.query.filter_by(result_id=result_id).all()
