from database import db

from models.student import Student
from models.result import Result
from models.mark import Mark
from models.subject import Subject
from models.exam import Exam


class StudentService:

    # ============================================================
    # FIND STUDENT BY USER ID
    # ============================================================

    @staticmethod
    def get_student_by_user_id(user_id):

        return Student.query.filter_by(
            user_id=user_id
        ).first()

    # ============================================================
    # FIND STUDENT BY USN
    # ============================================================

    @staticmethod
    def get_student_by_usn(usn):

        if not usn:
            return None

        return Student.query.filter_by(
            usn=usn.strip().upper()
        ).first()

    # ============================================================
    # FIND STUDENT BY USN
    #
    # Compatibility method used by validation/processing services.
    # ============================================================

    @staticmethod
    def find_by_usn(usn):

        if not usn:
            return None

        return Student.query.filter_by(
            usn=usn.strip().upper()
        ).first()

    # ============================================================
    # GET OR CREATE STUDENT
    #
    # ParsedStudent contains:
    #   usn
    #   name
    #   overall_result
    #   subjects
    #
    # Semester / section / department come from Exam.
    # ============================================================

    @staticmethod
    def get_or_create(parsed_student, exam):

        if not parsed_student.usn:
            raise ValueError(
                "Student USN is missing from parsed result"
            )

        usn = parsed_student.usn.strip().upper()

        # --------------------------------------------------------
        # Find existing student by USN
        # --------------------------------------------------------

        student = Student.query.filter_by(
            usn=usn
        ).first()

        if student:

            # Do not overwrite existing account information.
            # Fill missing academic information if necessary.

            if not student.name:
                student.name = parsed_student.name

            if student.semester is None:
                student.semester = exam.semester

            if student.section is None:
                student.section = exam.section

            if student.department_id is None:
                student.department_id = exam.department_id

            db.session.flush()

            return student

        # --------------------------------------------------------
        # Create new student
        # --------------------------------------------------------

        student = Student(
            user_id=None,
            usn=usn,
            name=parsed_student.name,
            semester=exam.semester,
            section=exam.section,
            cgpa=0.0,
            department_id=exam.department_id,
        )

        db.session.add(student)

        db.session.flush()

        return student

    # ============================================================
    # GET STUDENT PROFILE
    # ============================================================

    @staticmethod
    def get_profile(user_id):

        student = StudentService.get_student_by_user_id(
            user_id
        )

        if student is None:
            return None

        return {
            "id": student.id,
            "usn": student.usn,
            "name": student.name,
            "semester": student.semester,
            "section": student.section,
            "cgpa": student.cgpa,
            "department_id": student.department_id,
        }

    # ============================================================
    # GET ALL PUBLISHED RESULTS
    # ============================================================

    @staticmethod
    def get_results(user_id):

        student = StudentService.get_student_by_user_id(
            user_id
        )

        if student is None:
            return None

        results = Result.query.filter_by(
            student_id=student.id,
            published=True
        ).order_by(
            Result.created_at.desc()
        ).all()

        response = []

        for result in results:

            exam = Exam.query.get(
                result.exam_id
            )

            marks = Mark.query.filter_by(
                result_id=result.id
            ).all()

            mark_list = []

            for mark in marks:

                subject = Subject.query.get(
                    mark.subject_id
                )

                mark_list.append({
                    "id": mark.id,

                    "subject_id": mark.subject_id,

                    "subject_code": (
                        subject.subject_code
                        if subject
                        else None
                    ),

                    "subject_name": (
                        subject.subject_name
                        if subject
                        else None
                    ),

                    "credits": (
                        subject.credits
                        if subject
                        else None
                    ),

                    "internal": mark.internal,

                    "external": mark.external,

                    "total": mark.total,

                    "result": mark.result,
                })

            response.append({
                "id": result.id,

                "exam": {
                    "id": (
                        exam.id
                        if exam
                        else None
                    ),

                    "academic_year": (
                        exam.academic_year
                        if exam
                        else None
                    ),

                    "semester": (
                        exam.semester
                        if exam
                        else None
                    ),

                    "section": (
                        exam.section
                        if exam
                        else None
                    ),

                    "exam_type": (
                        exam.exam_type
                        if exam
                        else None
                    ),

                    "exam_month": (
                        exam.exam_month
                        if exam
                        else None
                    ),

                    "exam_year": (
                        exam.exam_year
                        if exam
                        else None
                    ),
                },

                "sgpa": result.sgpa,

                "cgpa": result.cgpa,

                "overall_result": result.overall_result,

                "published": result.published,

                "marks": mark_list,

                "created_at": (
                    result.created_at.isoformat()
                    if result.created_at
                    else None
                ),
            })

        return response

    # ============================================================
    # GET SINGLE PUBLISHED RESULT
    # ============================================================

    @staticmethod
    def get_result(user_id, result_id):

        student = StudentService.get_student_by_user_id(
            user_id
        )

        if student is None:
            return None

        result = Result.query.filter_by(
            id=result_id,
            student_id=student.id,
            published=True
        ).first()

        if result is None:
            return None

        exam = Exam.query.get(
            result.exam_id
        )

        marks = Mark.query.filter_by(
            result_id=result.id
        ).all()

        mark_list = []

        for mark in marks:

            subject = Subject.query.get(
                mark.subject_id
            )

            mark_list.append({
                "id": mark.id,

                "subject_id": mark.subject_id,

                "subject_code": (
                    subject.subject_code
                    if subject
                    else None
                ),

                "subject_name": (
                    subject.subject_name
                    if subject
                    else None
                ),

                "credits": (
                    subject.credits
                    if subject
                    else None
                ),

                "internal": mark.internal,

                "external": mark.external,

                "total": mark.total,

                "result": mark.result,
            })

        return {
            "id": result.id,

            "exam": {
                "id": (
                    exam.id
                    if exam
                    else None
                ),

                "academic_year": (
                    exam.academic_year
                    if exam
                    else None
                ),

                "semester": (
                    exam.semester
                    if exam
                    else None
                ),

                "section": (
                    exam.section
                    if exam
                    else None
                ),

                "exam_type": (
                    exam.exam_type
                    if exam
                    else None
                ),

                "exam_month": (
                    exam.exam_month
                    if exam
                    else None
                ),

                "exam_year": (
                    exam.exam_year
                    if exam
                    else None
                ),
            },

            "sgpa": result.sgpa,

            "cgpa": result.cgpa,

            "overall_result": result.overall_result,

            "published": result.published,

            "marks": mark_list,

            "created_at": (
                result.created_at.isoformat()
                if result.created_at
                else None
            ),
        }