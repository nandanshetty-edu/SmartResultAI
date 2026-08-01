from database import db


class Teacher(db.Model):

    __tablename__ = "teachers"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    employee_id = db.Column(
        db.String(30),
        unique=True
    )

    name = db.Column(db.String(150))

    designation = db.Column(db.String(100))

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )