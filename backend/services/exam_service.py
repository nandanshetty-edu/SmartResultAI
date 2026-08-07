from database import db
from models.exam import Exam


class ExamService:

    @staticmethod
    def get_or_create(
        academic_year,
        semester,
        section,
        exam_type,
        exam_month,
        exam_year,
        department_id,
        created_by,
    ):

        exam = Exam.query.filter_by(
            academic_year=academic_year,
            semester=semester,
            section=section,
            exam_type=exam_type,
            exam_month=exam_month,
            exam_year=exam_year,
            department_id=department_id,
        ).first()

        if exam:
            return exam

        exam = Exam(
            academic_year=academic_year,
            semester=semester,
            section=section,
            exam_type=exam_type,
            exam_month=exam_month,
            exam_year=exam_year,
            department_id=department_id,
            created_by=created_by,
        )

        db.session.add(exam)
        db.session.commit()

        return exam

    @staticmethod
    def get_all():

        return Exam.query.order_by(
            Exam.id.desc()
        ).all()

    @staticmethod
    def get_by_id(exam_id):

        return Exam.query.get(exam_id)