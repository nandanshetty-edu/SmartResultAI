from app import app
from database import db

from models.result import Result
from models.student import Student

from services.gpa_service import GPAService


with app.app_context():

    results = Result.query.order_by(
        Result.id
    ).all()

    print()
    print("=" * 70)
    print("SMARTRESULT AI - GPA BACKFILL")
    print("=" * 70)

    print(
        f"Results found: {len(results)}"
    )

    updated = 0

    try:

        for result in results:

            # ----------------------------------------------------
            # Calculate SGPA + CGPA
            # ----------------------------------------------------

            GPAService.update_result_gpa(
                result
            )

            # ----------------------------------------------------
            # Find student
            # ----------------------------------------------------

            student = db.session.get(
                Student,
                result.student_id
            )

            if student:

                student.cgpa = (
                    result.cgpa
                )

            updated += 1

            print(
                f"Result {result.id:>3} | "
                f"Student {result.student_id:>3} | "
                f"SGPA: {result.sgpa:.2f} | "
                f"CGPA: {result.cgpa:.2f}"
            )

        # --------------------------------------------------------
        # Commit everything
        # --------------------------------------------------------

        db.session.commit()

        print()
        print("=" * 70)
        print(
            f"SUCCESS: {updated} results updated"
        )
        print("=" * 70)

    except Exception as e:

        db.session.rollback()

        print()
        print("=" * 70)
        print("BACKFILL FAILED")
        print("=" * 70)

        print(
            f"Error: {e}"
        )

        raise