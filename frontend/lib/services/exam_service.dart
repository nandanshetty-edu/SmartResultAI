import '../core/api/api_client.dart';
import '../models/exam.dart';

class ExamService {
  static Future<List<Exam>> getExams() async {
    final response = await ApiClient.dio.get(
      "/exams/",
    );

    final List data = response.data["data"];

    return data
        .map(
          (e) => Exam.fromJson(e),
        )
        .toList();
  }
}