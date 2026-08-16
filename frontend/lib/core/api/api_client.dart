import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class ApiClient {
  ApiClient._();

  static const String baseUrl =
      "http://127.0.0.1:5000/api";

  static const FlutterSecureStorage _storage =
      FlutterSecureStorage();

  static final Dio dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,

      connectTimeout:
          const Duration(seconds: 60),

      receiveTimeout:
          const Duration(seconds: 60),

      sendTimeout:
          const Duration(seconds: 60),

      headers: {
        "Accept": "application/json",
      },
    ),
  );

  static Future<void> initialize() async {
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _storage.read(
            key: "access_token",
          );

          if (token != null && token.isNotEmpty) {
            options.headers["Authorization"] =
                "Bearer $token";
          }

          handler.next(options);
        },
      ),
    );
  }
}