from database import db
from models.subject import Subject


class SubjectService:

    @staticmethod
    def get_or_create(subject_code, semester, department_id):

        subject = Subject.query.filter_by(
            subject_code=subject_code
        ).first()

        if subject:
            return subject

        subject = Subject(
            subject_code=subject_code,
            semester=semester,
            department_id=department_id
        )

        db.session.add(subject)
        db.session.commit()

        return subject

    @staticmethod
    def get_by_id(subject_id):

        return Subject.query.get(subject_id)