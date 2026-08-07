import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../../models/exam.dart';
import '../../services/exam_service.dart';
import '../../services/processing_service.dart';
import '../download/download_screen.dart';

import 'widgets/process_button.dart';
import 'widgets/status_card.dart';
import 'widgets/upload_card.dart';

class UploadScreen extends StatefulWidget {
  const UploadScreen({super.key});

  @override
  State<UploadScreen> createState() => _UploadScreenState();
}

class _UploadScreenState extends State<UploadScreen> {
  PlatformFile? pdfFile;
  PlatformFile? excelFile;

  bool loading = false;

  String status = "🤖 AI Assistant is waiting for your files.";

  List<Exam> exams = [];

  Exam? selectedExam;

  @override
  void initState() {
    super.initState();
    loadExams();
  }

  Future<void> loadExams() async {
    try {
      final data = await ExamService.getExams();

      if (!mounted) return;

      setState(() {
        exams = data;
      });
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text("Failed to load exams\n$e"),
        ),
      );
    }
  }

  Future<void> pickPdf() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ["pdf"],
    );

    if (result != null && mounted) {
      setState(() {
        pdfFile = result.files.first;
      });
    }
  }

  Future<void> pickExcel() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ["xlsx"],
    );

    if (result != null && mounted) {
      setState(() {
        excelFile = result.files.first;
      });
    }
  }

  Future<void> process() async {
    if (pdfFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please select the Result PDF."),
        ),
      );
      return;
    }

    if (excelFile == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please select the Excel template."),
        ),
      );
      return;
    }

    if (selectedExam == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Please select an exam."),
        ),
      );
      return;
    }

    try {
      setState(() {
        loading = true;
        status = "📤 Uploading files...";
      });

      final result = await ProcessingService.process(
        pdfPath: pdfFile!.path!,
        excelPath: excelFile!.path!,
        examId: selectedExam!.id,
      );

      if (!mounted) return;

      setState(() {
        loading = false;
        status = "✅ Processing Completed Successfully!";
      });

      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => DownloadScreen(
            response: result,
          ),
        ),
      );
    } catch (e) {
      if (!mounted) return;

      setState(() {
        loading = false;
        status = "❌ Processing Failed";
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            e.toString().replaceFirst("Exception: ", ""),
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final desktop = MediaQuery.of(context).size.width > 900;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Process Results"),
      ),
      backgroundColor: const Color(0xffF8FAFC),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(
              maxWidth: 1200,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Upload VTU Result Files",
                  style: Theme.of(context).textTheme.headlineMedium,
                ),

                const SizedBox(height: 8),

                const Text(
                  "Upload the Result PDF and Excel template to automatically generate the completed result sheet.",
                ),

                const SizedBox(height: 30),

                desktop
                    ? Row(
                        children: [
                          Expanded(
                            child: UploadCard(
                              title: "Result PDF",
                              subtitle: "Click to upload PDF",
                              icon: Icons.picture_as_pdf,
                              color: Colors.red,
                              fileName: pdfFile?.name,
                              onTap: pickPdf,
                            ),
                          ),
                          const SizedBox(width: 20),
                          Expanded(
                            child: UploadCard(
                              title: "Excel Template",
                              subtitle: "Click to upload Excel",
                              icon: Icons.table_chart,
                              color: Colors.green,
                              fileName: excelFile?.name,
                              onTap: pickExcel,
                            ),
                          ),
                        ],
                      )
                    : Column(
                        children: [
                          UploadCard(
                            title: "Result PDF",
                            subtitle: "Click to upload PDF",
                            icon: Icons.picture_as_pdf,
                            color: Colors.red,
                            fileName: pdfFile?.name,
                            onTap: pickPdf,
                          ),
                          const SizedBox(height: 20),
                          UploadCard(
                            title: "Excel Template",
                            subtitle: "Click to upload Excel",
                            icon: Icons.table_chart,
                            color: Colors.green,
                            fileName: excelFile?.name,
                            onTap: pickExcel,
                          ),
                        ],
                      ),

                const SizedBox(height: 30),

                DropdownButtonFormField<Exam>(
                  value: selectedExam,
                  decoration: const InputDecoration(
                    labelText: "Select Exam",
                    prefixIcon: Icon(Icons.school),
                    border: OutlineInputBorder(),
                  ),
                  items: exams.map((exam) {
                    return DropdownMenuItem<Exam>(
                      value: exam,
                      child: Text(exam.displayName),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      selectedExam = value;
                    });
                  },
                ),

                const SizedBox(height: 30),

                StatusCard(
                  status: status,
                ),

                const SizedBox(height: 30),

                ProcessButton(
                  loading: loading,
                  onPressed: process,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}