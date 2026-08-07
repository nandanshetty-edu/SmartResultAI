import 'package:flutter/material.dart';

class ExamDropdown extends StatelessWidget {
  final String? value;
  final List<String> items;
  final ValueChanged<String?> onChanged;

  const ExamDropdown({
    super.key,
    required this.value,
    required this.items,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      value: value,
      decoration: const InputDecoration(
        labelText: "Select Exam",
        prefixIcon: Icon(Icons.school),
      ),
      items: items
          .map(
            (exam) => DropdownMenuItem(
              value: exam,
              child: Text(exam),
            ),
          )
          .toList(),
      onChanged: onChanged,
    );
  }
}