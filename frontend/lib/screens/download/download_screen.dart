import 'dart:io';
import 'dart:typed_data';

import 'package:file_selector/file_selector.dart';
import 'package:flutter/material.dart';
import 'package:open_filex/open_filex.dart';

import '../../services/download_service.dart';

class DownloadScreen extends StatefulWidget {
  final Map<String, dynamic> response;

  const DownloadScreen({
    super.key,
    required this.response,
  });

  @override
  State<DownloadScreen> createState() => _DownloadScreenState();
}

class _DownloadScreenState extends State<DownloadScreen> {
  bool downloading = false;

  Future<void> downloadExcel() async {
    try {
      setState(() {
        downloading = true;
      });

      final filename = widget.response["filename"];

      Uint8List bytes = await DownloadService.downloadFile(
        filename,
      );

      final String? path = await getSaveLocation(
        suggestedName: filename,
      ).then(
        (location) => location?.path,
      );

      if (path == null) {
        setState(() {
          downloading = false;
        });
        return;
      }

      final file = File(path);

      await file.writeAsBytes(bytes);

      if (!mounted) return;

      setState(() {
        downloading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "Excel downloaded successfully.",
          ),
        ),
      );

      await OpenFilex.open(file.path);
    } catch (e) {
      setState(() {
        downloading = false;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            e.toString(),
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final summary = widget.response["summary"];

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Download Result",
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(30),
          child: SizedBox(
            width: 500,
            child: Card(
              elevation: 5,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(20),
              ),
              child: Padding(
                padding: const EdgeInsets.all(30),
                child: Column(
                  children: [

                    const Icon(
                      Icons.check_circle,
                      color: Colors.green,
                      size: 100,
                    ),

                    const SizedBox(height: 20),

                    const Text(
                      "Processing Completed",
                      style: TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 10),

                    const Text(
                      "Result generated successfully.",
                    ),

                    const Divider(height: 40),

                    ListTile(
                      leading: const Icon(Icons.people),
                      title: const Text("Students"),
                      trailing: Text(
                        summary["students"].toString(),
                      ),
                    ),

                    ListTile(
                      leading: const Icon(Icons.assignment),
                      title: const Text("Results"),
                      trailing: Text(
                        summary["results"].toString(),
                      ),
                    ),

                    ListTile(
                      leading: const Icon(Icons.school),
                      title: const Text("Marks"),
                      trailing: Text(
                        summary["marks"].toString(),
                      ),
                    ),

                    const SizedBox(height: 30),

                    SizedBox(
                      width: double.infinity,
                      height: 55,
                      child: ElevatedButton.icon(
                        onPressed:
                            downloading ? null : downloadExcel,
                        icon: downloading
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child:
                                    CircularProgressIndicator(
                                  strokeWidth: 2,
                                  color: Colors.white,
                                ),
                              )
                            : const Icon(
                                Icons.download,
                              ),
                        label: Text(
                          downloading
                              ? "Downloading..."
                              : "Download Excel",
                        ),
                      ),
                    ),

                    const SizedBox(height: 15),

                    SizedBox(
                      width: double.infinity,
                      height: 55,
                      child: OutlinedButton.icon(
                        onPressed: () {
                          Navigator.popUntil(
                            context,
                            (route) => route.isFirst,
                          );
                        },
                        icon: const Icon(Icons.home),
                        label: const Text(
                          "Back to Dashboard",
                        ),
                      ),
                    ),

                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}