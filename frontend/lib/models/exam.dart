class Exam {
  final int id;
  final String academicYear;
  final int semester;
  final String? section;
  final String examType;
  final String examMonth;
  final int examYear;

  Exam({
    required this.id,
    required this.academicYear,
    required this.semester,
    this.section,
    required this.examType,
    required this.examMonth,
    required this.examYear,
  });

  factory Exam.fromJson(Map<String, dynamic> json) {
    return Exam(
      id: json["id"],
      academicYear: json["academic_year"],
      semester: json["semester"],
      section: json["section"],
      examType: json["exam_type"],
      examMonth: json["exam_month"],
      examYear: json["exam_year"],
    );
  }

  String get displayName {
    return "Semester $semester • $examType • $examMonth $examYear";
  }
}