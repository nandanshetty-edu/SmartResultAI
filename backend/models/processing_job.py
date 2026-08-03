from database import db
from datetime import datetime


class ProcessingJob(db.Model):

    __tablename__ = "processing_jobs"

    id = db.Column(db.Integer, primary_key=True)

    job_code = db.Column(db.String(50), unique=True, nullable=False)

    teacher_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    exam_id = db.Column(db.Integer, db.ForeignKey("exams.id"), nullable=False)

    pdf_path = db.Column(db.String(300))

    excel_template_path = db.Column(db.String(300))

    output_excel_path = db.Column(db.String(300))

    status = db.Column(db.String(30), default="PENDING")

    total_students = db.Column(db.Integer, default=0)

    processed_students = db.Column(db.Integer, default=0)

    failed_students = db.Column(db.Integer, default=0)

    error_message = db.Column(db.Text)

    started_at = db.Column(db.DateTime, default=datetime.utcnow)

    completed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<ProcessingJob {self.job_code}>"
