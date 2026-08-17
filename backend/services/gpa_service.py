from database import db

from models.mark import Mark
from models.subject import Subject
from models.result import Result
from models.student import Student


class GPAService:

    # ============================================================
    # VTU 2025 GRADE POINT
    #
    # O  = 10
    # A+ = 9
    # A  = 8
    # B+ = 7
    # B  = 6
    # C  = 5
    # P  = 4
    # F  = 0
    #
    # Mark ranges:
    #
    # 90-100 -> O
    # 80-89  -> A+
    # 70-79  -> A
    # 60-69  -> B+
    # 55-59  -> B
    # 50-54  -> C
    # 40-49  -> P
    # 0-39   -> F
    # ============================================================

    @staticmethod
    def grade_point_from_total(total):

        if total is None:
            return 0

        try:
            total = float(total)

        except (TypeError, ValueError):
            return 0

        if total >= 90:
            return 10

        if total >= 80:
            return 9

        if total >= 70:
            return 8

        if total >= 60:
            return 7

        if total >= 55:
            return 6

        if total >= 50:
            return 5

        if total >= 40:
            return 4

        return 0

    # ============================================================
    # CALCULATE SGPA
    # ============================================================

    @classmethod
    def calculate_sgpa(cls, result):

        if result is None:
            raise ValueError(
                "Result is required"
            )

        marks = Mark.query.filter_by(
            result_id=result.id
        ).all()

        total_credit_points = 0.0
        total_credits = 0.0

        for mark in marks:

            # SQLAlchemy 2.x compatible lookup
            subject = db.session.get(
                Subject,
                mark.subject_id
            )

            if subject is None:
                continue

            credits = subject.credits

            # Ignore non-credit subjects.
            if credits is None or credits <= 0:
                continue

            grade_point = (
                cls.grade_point_from_total(
                    mark.total
                )
            )

            total_credit_points += (
                credits * grade_point
            )

            total_credits += credits

        if total_credits == 0:
            return 0.0

        sgpa = (
            total_credit_points /
            total_credits
        )

        return round(sgpa, 2)

    # ============================================================
    # CALCULATE CGPA
    # ============================================================

    @classmethod
    def calculate_cgpa(cls, student):

        if student is None:
            raise ValueError(
                "Student is required"
            )

        results = Result.query.filter_by(
            student_id=student.id
        ).order_by(
            Result.created_at.asc()
        ).all()

        total_credit_points = 0.0
        total_credits = 0.0

        for result in results:

            marks = Mark.query.filter_by(
                result_id=result.id
            ).all()

            for mark in marks:

                subject = db.session.get(
                    Subject,
                    mark.subject_id
                )

                if subject is None:
                    continue

                credits = subject.credits

                # Ignore non-credit subjects.
                if credits is None or credits <= 0:
                    continue

                grade_point = (
                    cls.grade_point_from_total(
                        mark.total
                    )
                )

                # ------------------------------------------------
                # Failed courses are not included in the
                # CGPA denominator.
                # ------------------------------------------------

                is_fail = (
                    str(mark.result or "")
                    .strip()
                    .upper()
                    in {
                        "F",
                        "FAIL"
                    }
                )

                if grade_point == 0 or is_fail:
                    continue

                total_credit_points += (
                    credits * grade_point
                )

                total_credits += credits

        if total_credits == 0:
            return 0.0

        cgpa = (
            total_credit_points /
            total_credits
        )

        return round(cgpa, 2)

    # ============================================================
    # UPDATE RESULT GPA
    # ============================================================

    @classmethod
    def update_result_gpa(cls, result):

        if result is None:
            raise ValueError(
                "Result is required"
            )

        # --------------------------------------------------------
        # Current semester SGPA
        # --------------------------------------------------------

        result.sgpa = (
            cls.calculate_sgpa(result)
        )

        # --------------------------------------------------------
        # Find student
        # --------------------------------------------------------

        student = db.session.get(
            Student,
            result.student_id
        )

        if student is None:
            raise ValueError(
                f"Student {result.student_id} "
                f"not found"
            )

        # --------------------------------------------------------
        # Cumulative CGPA
        # --------------------------------------------------------

        result.cgpa = (
            cls.calculate_cgpa(student)
        )

        # Keep student's current CGPA synchronized.
        student.cgpa = result.cgpa

        db.session.flush()

        return result