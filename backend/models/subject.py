from database import db


class Subject(db.Model):

    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    subject_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    subject_name = db.Column(db.String(200))

    credits = db.Column(db.Integer)

    semester = db.Column(db.Integer)

    department_id = db.Column(
        db.Integer,
        db.ForeignKey("departments.id")
    )