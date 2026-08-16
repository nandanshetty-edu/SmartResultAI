import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../dashboard/dashboard_screen.dart';
import '../student/student_dashboard.dart';

import 'glass_card.dart';
import 'login_animation.dart';
import 'login_form.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  Future<void> handleLogin(
    BuildContext context,
    Map<String, dynamic> response,
  ) async {
    if (!context.mounted) return;

    final user = response["user"];

    if (user == null || user is! Map) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "Invalid login response from server.",
          ),
        ),
      );

      return;
    }

    final role = user["role"]?.toString().toUpperCase();

    if (role == "TEACHER") {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const DashboardScreen(),
        ),
      );

      return;
    }

    if (role == "STUDENT") {
      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => const StudentDashboard(),
        ),
      );

      return;
    }

    if (role == "ADMIN") {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text(
            "Admin dashboard is not available yet.",
          ),
        ),
      );

      return;
    }

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(
          "Unknown user role: ${role ?? "none"}",
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isDesktop =
        MediaQuery.of(context).size.width > 900;

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            colors: [
              Color(0xff2563EB),
              Color(0xff4F46E5),
            ],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
        ),

        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(30),

              child: ConstrainedBox(
                constraints: const BoxConstraints(
                  maxWidth: 1200,
                ),

                child: isDesktop
                    ? _DesktopLogin(
                        onLogin: (response) {
                          return handleLogin(
                            context,
                            response,
                          );
                        },
                      )
                    : _MobileLogin(
                        onLogin: (response) {
                          return handleLogin(
                            context,
                            response,
                          );
                        },
                      ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}


// ============================================================
// DESKTOP LOGIN
// ============================================================

class _DesktopLogin extends StatelessWidget {
  final Future<void> Function(
    Map<String, dynamic> response,
  ) onLogin;

  const _DesktopLogin({
    required this.onLogin,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          flex: 5,

          child: const LoginAnimation()
              .animate()
              .fadeIn(
                duration: 700.ms,
              )
              .slideX(
                begin: -.2,
              ),
        ),

        const SizedBox(width: 60),

        Expanded(
          flex: 4,

          child: GlassCard(
            child: LoginForm(
              onLogin: onLogin,
            ),
          )
              .animate()
              .fadeIn(
                delay: 300.ms,
              )
              .slideX(
                begin: .3,
              ),
        ),
      ],
    );
  }
}


// ============================================================
// MOBILE LOGIN
// ============================================================

class _MobileLogin extends StatelessWidget {
  final Future<void> Function(
    Map<String, dynamic> response,
  ) onLogin;

  const _MobileLogin({
    required this.onLogin,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const SizedBox(height: 20),

        const LoginAnimation()
            .animate()
            .fadeIn()
            .scale(),

        const SizedBox(height: 40),

        GlassCard(
          child: LoginForm(
            onLogin: onLogin,
          ),
        )
            .animate()
            .fadeIn(
              delay: 300.ms,
            )
            .slideY(
              begin: .3,
            ),
      ],
    );
  }
}