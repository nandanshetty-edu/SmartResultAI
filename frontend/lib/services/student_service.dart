import 'package:dio/dio.dart';

import '../core/api/api_client.dart';

class StudentService {
  StudentService._();

  static Future<Map<String, dynamic>> getProfile() async {
    try {
      final response = await ApiClient.dio.get(
        "/student/profile",
      );

      final data = Map<String, dynamic>.from(
        response.data,
      );

      if (data["success"] != true) {
        throw Exception(
          data["message"] ??
              "Failed to load student profile",
        );
      }

      return Map<String, dynamic>.from(
        data["student"],
      );
    } on DioException catch (e) {
      throw Exception(
        _getErrorMessage(e),
      );
    }
  }

  static Future<List<Map<String, dynamic>>> getResults() async {
    try {
      final response = await ApiClient.dio.get(
        "/student/results",
      );

      final data = Map<String, dynamic>.from(
        response.data,
      );

      if (data["success"] != true) {
        throw Exception(
          data["message"] ??
              "Failed to load results",
        );
      }

      final results = data["results"];

      if (results is! List) {
        return [];
      }

      return results
          .map(
            (item) => Map<String, dynamic>.from(
              item,
            ),
          )
          .toList();
    } on DioException catch (e) {
      throw Exception(
        _getErrorMessage(e),
      );
    }
  }

  static String _getErrorMessage(
    DioException e,
  ) {
    if (e.response?.data is Map) {
      final data =
          Map<String, dynamic>.from(
        e.response!.data,
      );

      return data["message"]?.toString() ??
          data["msg"]?.toString() ??
          "Request failed";
    }

    if (e.type == DioExceptionType.connectionError) {
      return "Unable to connect to SmartResult AI server.";
    }

    return e.message ??
        "Something went wrong.";
  }
}