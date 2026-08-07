import 'package:dio/dio.dart';

class ApiClient {
  ApiClient._();

  static const String baseUrl = "http://127.0.0.1:5000/api";

  // Android Emulator
  // static const String baseUrl = "http://10.0.2.2:5000/api";

  static final Dio dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 60),
      receiveTimeout: const Duration(seconds: 60),
      sendTimeout: const Duration(seconds: 60),
      headers: {
        "Accept": "application/json",
      },
    ),
  );
}