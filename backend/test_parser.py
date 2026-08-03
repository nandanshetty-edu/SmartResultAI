from services.parser.camelot_parser import CamelotParser

students = CamelotParser.parse("sample_data/pdf/Poornima_merged.pdf")

print()

print("Students Found :", len(students))

print()

student = students[0]

print("USN :", student.usn)
print("Name :", student.name)
print("Overall Result :", student.overall_result)

print("\nSubjects\n")

for subject in student.subjects.values():

    print(
        subject.subject_code,
        subject.internal,
        subject.external,
        subject.total,
        subject.result,
    )
