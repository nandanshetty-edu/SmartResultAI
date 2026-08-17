from typing import Optional


class VTUService:

    # ============================================================
    # VTU 2025 SCHEME
    # II SEMESTER
    #
    # Source:
    # VTU B.E./B.Tech 2025 Scheme
    #
    # IMPORTANT:
    # Soft Skills (1BSKS206) is PP / non-credit.
    # ============================================================

    SUBJECTS = {

        # --------------------------------------------------------
        # 1BCEDS203
        # --------------------------------------------------------

        "1BCEDS203": {
            "subject_name":
                "Computer-Aided Engineering Drawing",
            "credits": 3,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # 1BEIT205
        #
        # Programme Specific Course
        # --------------------------------------------------------

        "1BEIT205": {
            "subject_name":
                "Programming in C",
            "credits": 3,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # 1BESC204C
        # --------------------------------------------------------

        "1BESC204C": {
            "subject_name":
                "Introduction to Electronics & "
                "Communication Engineering",
            "credits": 3,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # BALake KANNADA
        # --------------------------------------------------------

        "1BKBK209": {
            "subject_name":
                "Balake Kannada",
            "credits": 1,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # SAMSKRUTIKA KANNADA
        # --------------------------------------------------------

        "1BKSK209": {
            "subject_name":
                "Samskrutika Kannada",
            "credits": 1,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # MATHEMATICS
        # --------------------------------------------------------

        "1BMATS201": {
            "subject_name":
                "Numerical Methods: CSE Stream",
            "credits": 4,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # PHYSICS
        # --------------------------------------------------------

        "1BPHYS202": {
            "subject_name":
                "Applied Physics",
            "credits": 4,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # PROGRAM-SPECIFIC LAB
        # --------------------------------------------------------

        "1BPOPL207": {
            "subject_name":
                "Programming in C Lab",
            "credits": 1,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # PROJECT
        # --------------------------------------------------------

        "1BPRJ258": {
            "subject_name":
                "Interdisciplinary Project-Based Learning",
            "credits": 1,
            "credit_type": "CREDIT"
        },

        # --------------------------------------------------------
        # SOFT SKILLS
        #
        # VTU marks this as PP / NCMC.
        # It does NOT contribute to SGPA / CGPA.
        # --------------------------------------------------------

        "1BSKS206": {
            "subject_name":
                "Soft Skills",
            "credits": 0,
            "credit_type": "NON_CREDIT"
        },
    }

    # ============================================================
    # NORMALIZE CODE
    # ============================================================

    @staticmethod
    def normalize_code(subject_code: str) -> str:

        if not subject_code:
            return ""

        return (
            str(subject_code)
            .replace("\n", "")
            .replace("\r", "")
            .replace(" ", "")
            .strip()
            .upper()
        )

    # ============================================================
    # GET METADATA
    # ============================================================

    @classmethod
    def get_subject_metadata(
        cls,
        subject_code: str
    ) -> Optional[dict]:

        code = cls.normalize_code(
            subject_code
        )

        return cls.SUBJECTS.get(code)

    # ============================================================
    # GET CREDITS
    # ============================================================

    @classmethod
    def get_credits(
        cls,
        subject_code: str
    ) -> Optional[int]:

        metadata = cls.get_subject_metadata(
            subject_code
        )

        if metadata is None:
            return None

        return metadata["credits"]

    # ============================================================
    # GET SUBJECT NAME
    # ============================================================

    @classmethod
    def get_subject_name(
        cls,
        subject_code: str
    ) -> Optional[str]:

        metadata = cls.get_subject_metadata(
            subject_code
        )

        if metadata is None:
            return None

        return metadata["subject_name"]

    # ============================================================
    # CHECK WHETHER SUBJECT IS KNOWN
    # ============================================================

    @classmethod
    def is_known_subject(
        cls,
        subject_code: str
    ) -> bool:

        return (
            cls.get_subject_metadata(
                subject_code
            ) is not None
        )