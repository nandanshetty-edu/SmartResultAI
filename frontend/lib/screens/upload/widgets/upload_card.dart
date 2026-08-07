import 'package:flutter/material.dart';

class UploadCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final IconData icon;
  final Color color;
  final String? fileName;
  final VoidCallback onTap;

  const UploadCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.icon,
    required this.color,
    required this.onTap,
    this.fileName,
  });

  @override
  Widget build(BuildContext context) {
    return InkWell(
      borderRadius: BorderRadius.circular(22),
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(25),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(22),
          border: Border.all(
            color: color.withOpacity(.25),
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.grey.withOpacity(.08),
              blurRadius: 12,
              offset: const Offset(0, 5),
            )
          ],
        ),
        child: Column(
          children: [
            CircleAvatar(
              radius: 35,
              backgroundColor: color.withOpacity(.15),
              child: Icon(
                icon,
                size: 35,
                color: color,
              ),
            ),
            const SizedBox(height: 18),
            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
            ),
            const SizedBox(height: 10),
            Text(
              fileName ?? subtitle,
              textAlign: TextAlign.center,
              style: TextStyle(
                color: fileName == null
                    ? Colors.grey
                    : Colors.green,
              ),
            ),
          ],
        ),
      ),
    );
  }
}