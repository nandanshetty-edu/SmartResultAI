from database import db


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    usn = db.Column(db.String(20), unique=True)

    name = db.Column(db.String(150))

    semester = db.Column(db.Integer)

    section = db.Column(db.String(5))

    cgpa = db.Column(db.Float, default=0.0)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )