from database import db


class Mark(db.Model):

    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)

    result_id = db.Column(
        db.Integer,
        db.ForeignKey("results.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    internal = db.Column(db.Integer)

    external = db.Column(db.Integer)

    total = db.Column(db.Integer)

    result = db.Column(db.String(5))