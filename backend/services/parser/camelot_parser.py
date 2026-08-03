import camelot

from services.parser.models import ParsedStudent, ParsedSubject

from services.parser.utils import normalize_subject


class CamelotParser:

    @staticmethod
    def parse(pdf_path):

        print("=" * 60)
        print("Reading PDF...")
        print("=" * 60)

        tables = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

        print("Tables Found :", len(tables))

        students = []

        # Every student = 3 tables
        for i in range(0, len(tables), 3):

            try:
                header = tables[i].df
                marks = tables[i + 1].df

            except IndexError:
                continue

            student = CamelotParser.parse_student(header, marks)

            students.append(student)

        return students

    @staticmethod
    def parse_student(header, marks):

        usn = str(header.iloc[0, 1]).strip()

        name = str(header.iloc[1, 1]).strip()

        student = ParsedStudent(usn=usn, name=name, overall_result="PASS")

        student.subjects = CamelotParser.parse_subjects(marks)

        # Check overall result
        for subject in student.subjects.values():

            if subject.result == "F":
                student.overall_result = "FAIL"
                break

        return student

    @staticmethod
    def parse_subjects(df):

        subjects = {}

        # Skip header row
        for row in range(1, len(df)):

            try:

                code = normalize_subject(df.iloc[row, 0])

                internal = int(df.iloc[row, 2])

                external = int(df.iloc[row, 3])

                total = int(df.iloc[row, 4])

                result = str(df.iloc[row, 5]).strip()

            except Exception:
                continue

            subjects[code] = ParsedSubject(
                subject_code=code,
                internal=internal,
                external=external,
                total=total,
                result=result,
            )

        return subjects
