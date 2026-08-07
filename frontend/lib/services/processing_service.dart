import 'package:dio/dio.dart';

import '../core/api/api_client.dart';

class ProcessingService {
  static Future<Map<String, dynamic>> process({
    required String pdfPath,
    required String excelPath,
    required int examId,
  }) async {
    try {
      FormData formData = FormData.fromMap({
        "pdf": await MultipartFile.fromFile(
          pdfPath,
          filename: pdfPath.split('/').last,
        ),
        "excel": await MultipartFile.fromFile(
          excelPath,
          filename: excelPath.split('/').last,
        ),
        "exam_id": examId.toString(),
      });

      final response = await ApiClient.dio.post(
        "/processing/process",
        data: formData,
      );

      if (response.statusCode == 200) {
        return response.data;
      }

      throw Exception("Server returned ${response.statusCode}");
    } on DioException catch (e) {
      if (e.response != null) {
        throw Exception(
          e.response?.data["message"] ??
              e.response?.data["errors"]?.toString() ??
              "Server Error",
        );
      }

      throw Exception("Unable to connect to server.");
    } catch (e) {
      throw Exception(e.toString());
    }
  }
}