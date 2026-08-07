import 'dart:typed_data';

import 'package:dio/dio.dart';

import '../core/api/api_client.dart';

class DownloadService {
  static Future<Uint8List> downloadFile(
    String filename,
  ) async {
    try {
      final response = await ApiClient.dio.get(
        "/download/$filename",
        options: Options(
          responseType: ResponseType.bytes,
        ),
      );

      return Uint8List.fromList(response.data);
    } on DioException catch (e) {
      throw Exception(
        e.response?.statusMessage ??
            "Failed to download file.",
      );
    }
  }
}