from services.parser.camelot_parser import CamelotParser

students = CamelotParser.parse(
    "sample_data/pdf/Poornima_merged.pdf"
)

print(students[0].subjects.keys())