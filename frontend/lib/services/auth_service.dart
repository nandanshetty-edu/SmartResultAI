import 'package:dio/dio.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../core/api/api_client.dart';

class AuthService {
  AuthService._();

  static const FlutterSecureStorage _storage =
      FlutterSecureStorage();

  // ============================================================
  // STUDENT LOGIN
  //
  // USN + Password
  // ============================================================

  static Future<Map<String, dynamic>> loginStudent({
    required String usn,
    required String password,
  }) async {
    return _login(
      data: {
        "role": "STUDENT",
        "usn": usn.trim().toUpperCase(),
        "password": password,
      },
    );
  }

  // ============================================================
  // TEACHER LOGIN
  //
  // College Gmail + Password
  // ============================================================

  static Future<Map<String, dynamic>> loginTeacher({
    required String email,
    required String password,
  }) async {
    return _login(
      data: {
        "role": "TEACHER",
        "email": email.trim().toLowerCase(),
        "password": password,
      },
    );
  }

  // ============================================================
  // COMMON LOGIN REQUEST
  // ============================================================

  static Future<Map<String, dynamic>> _login({
    required Map<String, dynamic> data,
  }) async {
    try {
      final response = await ApiClient.dio.post(
        "/auth/login",
        data: data,
      );

      final responseData = Map<String, dynamic>.from(
        response.data,
      );

      // --------------------------------------------------------
      // Backend says login failed
      // --------------------------------------------------------

      if (responseData["success"] != true) {
        throw Exception(
          responseData["message"] ?? "Login failed",
        );
      }

      // --------------------------------------------------------
      // Get JWT
      // --------------------------------------------------------

      final token = responseData["token"];

      if (token == null || token.toString().isEmpty) {
        throw Exception(
          "Login succeeded but no JWT token was returned.",
        );
      }

      // --------------------------------------------------------
      // Save JWT securely
      // --------------------------------------------------------

      await _storage.write(
        key: "access_token",
        value: token.toString(),
      );

      // --------------------------------------------------------
      // Get user
      // --------------------------------------------------------

      final user = responseData["user"];

      if (user is Map) {
        // Save role
        if (user["role"] != null) {
          await _storage.write(
            key: "user_role",
            value: user["role"].toString(),
          );
        }

        // Save email if available
        if (user["email"] != null) {
          await _storage.write(
            key: "user_email",
            value: user["email"].toString(),
          );
        }

        // Save student USN if available
        final student = user["student"];

        if (student is Map &&
            student["usn"] != null) {
          await _storage.write(
            key: "user_usn",
            value: student["usn"].toString(),
          );
        }

        // Save teacher employee ID if available
        final teacher = user["teacher"];

        if (teacher is Map &&
            teacher["employee_id"] != null) {
          await _storage.write(
            key: "employee_id",
            value: teacher["employee_id"].toString(),
          );
        }
      }

      return responseData;
    }

    // ==========================================================
    // DIO ERROR
    // ==========================================================

    on DioException catch (e) {
      String message =
          "Unable to connect to server.";

      if (e.response != null) {
        final responseData = e.response!.data;

        if (responseData is Map &&
            responseData["message"] != null) {
          message =
              responseData["message"].toString();
        } else if (responseData is Map &&
            responseData["msg"] != null) {
          message =
              responseData["msg"].toString();
        } else if (e.response!.statusMessage != null) {
          message =
              e.response!.statusMessage!;
        }
      } else if (e.message != null) {
        message = e.message!;
      }

      throw Exception(message);
    }

    // ==========================================================
    // OTHER ERROR
    // ==========================================================

    catch (e) {
      throw Exception(
        e.toString().replaceFirst(
          "Exception: ",
          "",
        ),
      );
    }
  }

  // ============================================================
  // GET JWT
  // ============================================================

  static Future<String?> getToken() async {
    return _storage.read(
      key: "access_token",
    );
  }

  // ============================================================
  // GET ROLE
  // ============================================================

  static Future<String?> getRole() async {
    return _storage.read(
      key: "user_role",
    );
  }

  // ============================================================
  // GET EMAIL
  // ============================================================

  static Future<String?> getEmail() async {
    return _storage.read(
      key: "user_email",
    );
  }

  // ============================================================
  // GET STUDENT USN
  // ============================================================

  static Future<String?> getUsn() async {
    return _storage.read(
      key: "user_usn",
    );
  }

  // ============================================================
  // GET TEACHER EMPLOYEE ID
  // ============================================================

  static Future<String?> getEmployeeId() async {
    return _storage.read(
      key: "employee_id",
    );
  }

  // ============================================================
  // CHECK LOGIN
  // ============================================================

  static Future<bool> isLoggedIn() async {
    final token = await getToken();

    return token != null &&
        token.isNotEmpty;
  }

  // ============================================================
  // LOGOUT
  // ============================================================

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

    await _storage.delete(
      key: "user_usn",
    );

    await _storage.delete(
      key: "employee_id",
    );
  }
}