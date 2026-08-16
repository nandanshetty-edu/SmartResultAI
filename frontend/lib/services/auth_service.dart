import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../core/api/api_client.dart';

class AuthService {
  AuthService._();

  static const FlutterSecureStorage _storage =
      FlutterSecureStorage();

  /// Login using email + password.
  ///
  /// Returns the complete backend response.
  static Future<Map<String, dynamic>> login({
    required String email,
    required String password,
  }) async {
    try {
      final response = await ApiClient.dio.post(
        "/auth/login",
        data: {
          "email": email.trim(),
          "password": password,
        },
      );

      final data = Map<String, dynamic>.from(
        response.data,
      );

      if (data["success"] != true) {
        throw Exception(
          data["message"] ?? "Login failed",
        );
      }

      final token = data["token"];

      if (token == null || token.toString().isEmpty) {
        throw Exception(
          "Login succeeded but no JWT token was returned.",
        );
      }

      // Save JWT securely.
      await _storage.write(
        key: "access_token",
        value: token.toString(),
      );

      // Save role for quick local routing.
      final user = data["user"];

      if (user is Map && user["role"] != null) {
        await _storage.write(
          key: "user_role",
          value: user["role"].toString(),
        );
      }

      // Save email.
      if (user is Map && user["email"] != null) {
        await _storage.write(
          key: "user_email",
          value: user["email"].toString(),
        );
      }

      return data;
    } on DioException catch (e) {
      String message = "Unable to connect to server.";

      if (e.response != null) {
        final responseData = e.response!.data;

        if (responseData is Map &&
            responseData["message"] != null) {
          message = responseData["message"].toString();
        } else if (responseData is Map &&
            responseData["msg"] != null) {
          message = responseData["msg"].toString();
        } else if (e.response!.statusMessage != null) {
          message = e.response!.statusMessage!;
        }
      } else if (e.message != null) {
        message = e.message!;
      }

      throw Exception(message);
    } catch (e) {
      throw Exception(
        e.toString().replaceFirst("Exception: ", ""),
      );
    }
  }

  /// Get the stored JWT.
  static Future<String?> getToken() async {
    return _storage.read(
      key: "access_token",
    );
  }

  /// Get the stored role.
  static Future<String?> getRole() async {
    return _storage.read(
      key: "user_role",
    );
  }

  /// Get the stored email.
  static Future<String?> getEmail() async {
    return _storage.read(
      key: "user_email",
    );
  }

  /// Check whether a token exists.
  static Future<bool> isLoggedIn() async {
    final token = await getToken();

    return token != null && token.isNotEmpty;
  }

  /// Logout.
  static Future<void> logout() async {
    await _storage.delete(
      key: "access_token",
    );

    await _storage.delete(
      key: "user_role",
    );

    await _storage.delete(
      key: "user_email",
    );
  }
}