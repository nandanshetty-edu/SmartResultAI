import 'package:flutter/material.dart';

class LoginAnimation extends StatelessWidget {
  const LoginAnimation({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: const [
        Icon(
          Icons.auto_graph_rounded,
          size: 140,
          color: Colors.white,
        ),
        SizedBox(height: 20),
        Text(
          "SmartResult AI",
          style: TextStyle(
            fontSize: 34,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        SizedBox(height: 10),
        Text(
          "AI Powered Result Processing",
          style: TextStyle(
            fontSize: 18,
            color: Colors.white70,
          ),
        ),
      ],
    );
  }
}