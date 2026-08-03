from database import db
from models.student import Student


class StudentService:

    @staticmethod
    def get_or_create(parsed_student):

        student = Student.query.filter_by(usn=parsed_student.usn).first()

        if student:

            student.name = parsed_student.name

            db.session.commit()

            return student

        student = Student(usn=parsed_student.usn, name=parsed_student.name)

        db.session.add(student)
        db.session.commit()

        return student

    @staticmethod
    def find_by_usn(usn):

        return Student.query.filter_by(usn=usn).first()
