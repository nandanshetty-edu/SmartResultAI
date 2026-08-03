from database import db
from datetime import datetime


class Exam(db.Model):

    __tablename__ = "exams"

    id = db.Column(db.Integer, primary_key=True)

    academic_year = db.Column(db.String(20), nullable=False)

    semester = db.Column(db.Integer, nullable=False)

    section = db.Column(db.String(10), nullable=True)

    exam_type = db.Column(db.String(30), nullable=False)

    exam_month = db.Column(db.String(20), nullable=False)

    exam_year = db.Column(db.Integer, nullable=False)

    department_id = db.Column(
        db.Integer, db.ForeignKey("departments.id"), nullable=False
    )

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Exam {self.academic_year} Sem {self.semester}>"
