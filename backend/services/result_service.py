from database import db
from models.result import Result


class ResultService:

    # ============================================================
    # CREATE RESULT
    # ============================================================

    @staticmethod
    def create_result(
        student,
        exam,
        processing_job=None,
        overall_result="PASS"
    ):

        # Check if this student already has a result
        # for this particular exam.
        existing = ResultService.get_by_student_exam(
            student_id=student.id,
            exam_id=exam.id
        )

        if existing:

            # Update overall result if processing the
            # same exam again.
            existing.overall_result = overall_result

            db.session.flush()

            return existing

        # --------------------------------------------------------
        # Create new result
        # --------------------------------------------------------

        result = Result(
            student_id=student.id,

            exam_id=exam.id,

            processing_job_id=(
                processing_job.id
                if processing_job
                else None
            ),

            overall_result=overall_result,

            sgpa=0.0,

            cgpa=(
                student.cgpa
                if student.cgpa is not None
                else 0.0
            ),

            # IMPORTANT:
            # Student should not see result until
            # teacher publishes it.
            published=False
        )

        db.session.add(result)

        # Get result.id immediately so marks can
        # reference this result.
        db.session.flush()

        return result

    # ============================================================
    # GET RESULT BY STUDENT + EXAM
    # ============================================================

    @staticmethod
    def get_by_student_exam(
        student_id,
        exam_id
    ):

        return Result.query.filter_by(
            student_id=student_id,
            exam_id=exam_id
        ).first()

    # ============================================================
    # GET RESULT BY ID
    # ============================================================

    @staticmethod
    def get_by_id(result_id):

        return Result.query.filter_by(
            id=result_id
        ).first()

    # ============================================================
    # GET ALL RESULTS FOR STUDENT
    # ============================================================

    @staticmethod
    def get_by_student(student_id):

        return Result.query.filter_by(
            student_id=student_id
        ).order_by(
            Result.created_at.desc()
        ).all()

    # ============================================================
    # GET PUBLISHED RESULTS FOR STUDENT
    # ============================================================

    @staticmethod
    def get_published_by_student(student_id):

        return Result.query.filter_by(
            student_id=student_id,
            published=True
        ).order_by(
            Result.created_at.desc()
        ).all()

    # ============================================================
    # PUBLISH RESULT
    # ============================================================

    @staticmethod
    def publish(result):

        if result is None:
            raise ValueError(
                "Result not found"
            )

        result.published = True

        db.session.flush()

        return result

    # ============================================================
    # UNPUBLISH RESULT
    # ============================================================

    @staticmethod
    def unpublish(result):

        if result is None:
            raise ValueError(
                "Result not found"
            )

        result.published = False

        db.session.flush()

        return result

    # ============================================================
    # DELETE RESULT
    # ============================================================

    @staticmethod
    def delete(result):

        if result is None:
            return False

        db.session.delete(result)

        db.session.flush()

        return True