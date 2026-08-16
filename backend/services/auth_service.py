from database import db

from models.user import User
from models.teacher import Teacher
from models.student import Student

from utils.password_utils import hash_password, verify_password


class AuthService:

    # ============================================================
    # GET USER BY EMAIL
    # ============================================================

    @staticmethod
    def get_user_by_email(email):

        if not email:
            return None

        return User.query.filter_by(
            email=email.strip().lower()
        ).first()

    # ============================================================
    # GET USER BY ID
    # ============================================================

    @staticmethod
    def get_user_by_id(user_id):

        return User.query.get(user_id)

    # ============================================================
    # GET STUDENT BY USN
    # ============================================================

    @staticmethod
    def get_student_by_usn(usn):

        if not usn:
            return None

        return Student.query.filter_by(
            usn=usn.strip().upper()
        ).first()

    # ============================================================
    # CREATE USER
    # ============================================================

    @staticmethod
    def create_user(
        email,
        password,
        role,
        employee_id=None,
        name=None,
        designation=None,
        department_id=None,
        usn=None,
        semester=None,
        section=None,
    ):

        email = email.strip().lower()
        role = role.strip().upper()

        allowed_roles = {
            "ADMIN",
            "TEACHER",
            "STUDENT",
        }

        if role not in allowed_roles:
            raise ValueError(
                "Invalid role. Allowed roles: ADMIN, TEACHER, STUDENT"
            )

        # --------------------------------------------------------
        # Duplicate email
        # --------------------------------------------------------

        existing_user = AuthService.get_user_by_email(email)

        if existing_user:
            raise ValueError(
                "Email already exists"
            )

        # --------------------------------------------------------
        # Create User
        # --------------------------------------------------------

        user = User(
            email=email,
            password=hash_password(password),
            role=role,
            is_active=True,
        )

        db.session.add(user)

        db.session.flush()

        # --------------------------------------------------------
        # Teacher
        # --------------------------------------------------------

        if role == "TEACHER":

            if not employee_id:
                raise ValueError(
                    "employee_id is required for teacher"
                )

            if not name:
                raise ValueError(
                    "name is required for teacher"
                )

            existing_teacher = Teacher.query.filter_by(
                employee_id=employee_id
            ).first()

            if existing_teacher:
                raise ValueError(
                    "Employee ID already exists"
                )

            teacher = Teacher(
                user_id=user.id,
                employee_id=employee_id,
                name=name,
                designation=designation,
                department_id=department_id,
            )

            db.session.add(teacher)

        # --------------------------------------------------------
        # Student
        # --------------------------------------------------------

        elif role == "STUDENT":

            if not usn:
                raise ValueError(
                    "USN is required for student"
                )

            if not name:
                raise ValueError(
                    "name is required for student"
                )

            usn = usn.strip().upper()

            existing_student = Student.query.filter_by(
                usn=usn
            ).first()

            if existing_student:
                raise ValueError(
                    "USN already exists"
                )

            student = Student(
                user_id=user.id,
                usn=usn,
                name=name,
                semester=semester,
                section=section,
                department_id=department_id,
            )

            db.session.add(student)

        db.session.commit()

        return user

    # ============================================================
    # AUTHENTICATE TEACHER
    #
    # Teacher login:
    # College Gmail + password
    # ============================================================

    @staticmethod
    def authenticate_teacher(email, password):

        if not email or not password:
            raise ValueError(
                "College Gmail and password are required"
            )

        user = AuthService.get_user_by_email(email)

        if user is None:
            raise ValueError(
                "Invalid college Gmail or password"
            )

        if user.role != "TEACHER":
            raise ValueError(
                "This account is not registered as a teacher"
            )

        if not user.is_active:
            raise ValueError(
                "Teacher account is inactive"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise ValueError(
                "Invalid college Gmail or password"
            )

        return user

    # ============================================================
    # AUTHENTICATE STUDENT
    #
    # Student login:
    # USN + password
    # ============================================================

    @staticmethod
    def authenticate_student(usn, password):

        if not usn or not password:
            raise ValueError(
                "USN and password are required"
            )

        usn = usn.strip().upper()

        student = AuthService.get_student_by_usn(usn)

        if student is None:
            raise ValueError(
                "Invalid USN or password"
            )

        # Student must be linked to a User account.
        if student.user_id is None:
            raise ValueError(
                "Student account has not been activated yet"
            )

        user = AuthService.get_user_by_id(
            student.user_id
        )

        if user is None:
            raise ValueError(
                "Student account not found"
            )

        if user.role != "STUDENT":
            raise ValueError(
                "This account is not registered as a student"
            )

        if not user.is_active:
            raise ValueError(
                "Student account is inactive"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise ValueError(
                "Invalid USN or password"
            )

        return user

    # ============================================================
    # PROFILE
    # ============================================================

    @staticmethod
    def get_profile(user):

        # --------------------------------------------------------
        # Teacher
        # --------------------------------------------------------

        if user.role == "TEACHER":

            teacher = Teacher.query.filter_by(
                user_id=user.id
            ).first()

            if teacher is None:
                return None

            return {
                "id": teacher.id,
                "employee_id": teacher.employee_id,
                "name": teacher.name,
                "designation": teacher.designation,
                "department_id": teacher.department_id,
            }

        # --------------------------------------------------------
        # Student
        # --------------------------------------------------------

        if user.role == "STUDENT":

            student = Student.query.filter_by(
                user_id=user.id
            ).first()

            if student is None:
                return None

            return {
                "id": student.id,
                "usn": student.usn,
                "name": student.name,
                "semester": student.semester,
                "section": student.section,
                "cgpa": student.cgpa,
                "department_id": student.department_id,
            }

        # --------------------------------------------------------
        # Admin
        # --------------------------------------------------------

        return None

    # ============================================================
    # SERIALIZE USER
    # ============================================================

    @staticmethod
    def serialize_user(user):

        response = {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }

        profile = AuthService.get_profile(user)

        if user.role == "TEACHER":
            response["teacher"] = profile

        elif user.role == "STUDENT":
            response["student"] = profile

        return response