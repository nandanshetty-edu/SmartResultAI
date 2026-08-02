from database import db
from datetime import datetime


class Result(db.Model):

    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    exam_id = db.Column(
        db.Integer,
        db.ForeignKey("exams.id"),
        nullable=False
    )

    processing_job_id = db.Column(
        db.Integer,
        db.ForeignKey("processing_jobs.id"),
        nullable=False
    )

    sgpa = db.Column(db.Float, default=0.0)

    cgpa = db.Column(db.Float, default=0.0)

    overall_result = db.Column(db.String(10))

    published = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )