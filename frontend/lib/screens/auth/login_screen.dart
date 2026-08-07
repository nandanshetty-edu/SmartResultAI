import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../dashboard/dashboard_screen.dart';
import 'glass_card.dart';
import 'login_animation.dart';
import 'login_form.dart';

class LoginScreen extends StatelessWidget {
  const LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.of(context).size.width > 900;

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
                    ? const _DesktopLogin()
                    : const _MobileLogin(),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _DesktopLogin extends StatelessWidget {
  const _DesktopLogin();

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          flex: 5,
          child: const LoginAnimation()
              .animate()
              .fadeIn(duration: 700.ms)
              .slideX(begin: -.2),
        ),

        const SizedBox(width: 60),

        Expanded(
          flex: 4,
          child: GlassCard(
            child: LoginForm(
              onLogin: () {
                Navigator.pushReplacement(
                  context,
                  MaterialPageRoute(
                    builder: (_) => const DashboardScreen(),
                  ),
                );
              },
            ),
          )
              .animate()
              .fadeIn(delay: 300.ms)
              .slideX(begin: .3),
        ),
      ],
    );
  }
}

class _MobileLogin extends StatelessWidget {
  const _MobileLogin();

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
            onLogin: () {
              Navigator.pushReplacement(
                context,
                MaterialPageRoute(
                  builder: (_) => const DashboardScreen(),
                ),
              );
            },
          ),
        )
            .animate()
            .fadeIn(delay: 300.ms)
            .slideY(begin: .3),
      ],
    );
  }
}