from database import db
from models.student import Student


class StudentService:

    @staticmethod
    def get_or_create(parsed_student):

        # Check if student already exists
        student = Student.query.filter_by(
            usn=parsed_student.usn
        ).first()

        if student:

            # Update name in case it changed
            student.name = parsed_student.name

            db.session.commit()

            return student

        # Create new student
        student = Student(
            usn=parsed_student.usn,
            name=parsed_student.name
        )

        db.session.add(student)
        db.session.commit()

        return student