from database import db
from models.subject import Subject

from services.vtu_service import VTUService


class SubjectService:

    # ============================================================
    # GET OR CREATE SUBJECT
    # ============================================================

    @staticmethod
    def get_or_create(
        subject_code,
        semester,
        department_id
    ):

        if not subject_code:
            raise ValueError(
                "Subject code is required"
            )

        subject_code = (
            str(subject_code)
            .strip()
            .upper()
        )

        # --------------------------------------------------------
        # Get VTU metadata
        # --------------------------------------------------------

        metadata = VTUService.get_subject_metadata(
            subject_code
        )

        # --------------------------------------------------------
        # Find existing subject
        # --------------------------------------------------------

        subject = Subject.query.filter_by(
            subject_code=subject_code
        ).first()

        if subject:

            # Fill/update metadata if available.
            if metadata:

                if not subject.subject_name:
                    subject.subject_name = (
                        metadata["subject_name"]
                    )

                if subject.credits is None:
                    subject.credits = (
                        metadata["credits"]
                    )

            if subject.semester is None:
                subject.semester = semester

            if subject.department_id is None:
                subject.department_id = department_id

            db.session.flush()

            return subject

        # --------------------------------------------------------
        # Unknown subject
        # --------------------------------------------------------

        if metadata is None:

            raise ValueError(
                f"VTU metadata not found for subject "
                f"'{subject_code}'. "
                f"Add this subject to vtu_service.py "
                f"before processing results."
            )

        # --------------------------------------------------------
        # Create subject
        # --------------------------------------------------------

        subject = Subject(
            subject_code=subject_code,

            subject_name=metadata[
                "subject_name"
            ],

            credits=metadata[
                "credits"
            ],

            semester=semester,

            department_id=department_id,
        )

        db.session.add(subject)

        db.session.flush()

        return subject

    # ============================================================
    # GET BY ID
    # ============================================================

    @staticmethod
    def get_by_id(subject_id):

        return Subject.query.get(
            subject_id
        )

    # ============================================================
    # GET BY CODE
    # ============================================================

    @staticmethod
    def get_by_code(subject_code):

        if not subject_code:
            return None

        return Subject.query.filter_by(
            subject_code=subject_code.strip().upper()
        ).first()

    # ============================================================
    # UPDATE VTU METADATA
    # ============================================================

    @staticmethod
    def refresh_metadata(subject):

        if subject is None:
            return None

        metadata = VTUService.get_subject_metadata(
            subject.subject_code
        )

        if metadata is None:
            return subject

        subject.subject_name = (
            metadata["subject_name"]
        )

        subject.credits = (
            metadata["credits"]
        )

        db.session.flush()

        return subject