import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../upload/upload_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final isDesktop = MediaQuery.of(context).size.width > 900;

    return Scaffold(
      backgroundColor: const Color(0xffF8FAFC),
      appBar: AppBar(
        elevation: 0,
        backgroundColor: Colors.transparent,
        title: const Text(
          "SmartResult AI",
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            onPressed: () {},
            icon: const Icon(Icons.notifications_none),
          ),
          const SizedBox(width: 10),
          const CircleAvatar(
            backgroundColor: Color(0xff2563EB),
            child: Icon(
              Icons.person,
              color: Colors.white,
            ),
          ),
          const SizedBox(width: 20),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(
              maxWidth: 1400,
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildWelcomeCard(),

                const SizedBox(height: 30),

                _buildStats(isDesktop),

                const SizedBox(height: 30),

                _buildQuickActions(
                  context,
                  isDesktop,
                ),

                const SizedBox(height: 30),

                _buildAIInsights(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildWelcomeCard() {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [
            Color(0xff2563EB),
            Color(0xff4F46E5),
          ],
        ),
        borderRadius: BorderRadius.circular(25),
      ),
      child: Row(
        children: [
          const CircleAvatar(
            radius: 38,
            backgroundColor: Colors.white,
            child: Icon(
              Icons.auto_awesome,
              color: Color(0xff2563EB),
              size: 42,
            ),
          ),

          const SizedBox(width: 20),

          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Good Evening 👋",
                  style: TextStyle(
                    color: Colors.white70,
                    fontSize: 18,
                  ),
                ),
                SizedBox(height: 8),
                Text(
                  "Welcome to SmartResult AI",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 28,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 10),
                Text(
                  "AI Powered Result Processing Platform",
                  style: TextStyle(
                    color: Colors.white70,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    ).animate().fadeIn().slideY(begin: -.2);
  }

  Widget _buildStats(bool desktop) {
    final cards = [
      _statCard(
        "Students",
        "48",
        Icons.people_alt_rounded,
        Colors.blue,
      ),
      _statCard(
        "Results",
        "48",
        Icons.assignment_turned_in,
        Colors.green,
      ),
      _statCard(
        "Marks",
        "432",
        Icons.school,
        Colors.orange,
      ),
      _statCard(
        "Pass %",
        "98%",
        Icons.bar_chart,
        Colors.purple,
      ),
    ];

    return desktop
        ? Row(
            children: cards
                .map(
                  (e) => Expanded(
                    child: Padding(
                      padding: const EdgeInsets.all(8),
                      child: e,
                    ),
                  ),
                )
                .toList(),
          )
        : Column(children: cards);
  }

  Widget _statCard(
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(22),
      ),
      child: Padding(
        padding: const EdgeInsets.all(22),
        child: Column(
          children: [
            CircleAvatar(
              radius: 28,
              backgroundColor: color.withOpacity(.15),
              child: Icon(
                icon,
                color: color,
              ),
            ),
            const SizedBox(height: 18),
            Text(
              value,
              style: const TextStyle(
                fontSize: 30,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 5),
            Text(title),
          ],
        ),
      ),
    ).animate().fadeIn().scale();
  }

  Widget _buildQuickActions(
    BuildContext context,
    bool desktop,
  ) {
    final actions = [
      _actionButton(
        context,
        "Process Result",
        Icons.upload_file,
        Colors.blue,
        () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (_) => const UploadScreen(),
            ),
          );
        },
      ),
      _actionButton(
        context,
        "History",
        Icons.history,
        Colors.green,
        () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("History Module Coming Soon"),
            ),
          );
        },
      ),
      _actionButton(
        context,
        "Analytics",
        Icons.analytics,
        Colors.orange,
        () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Analytics Module Coming Soon"),
            ),
          );
        },
      ),
      _actionButton(
        context,
        "Settings",
        Icons.settings,
        Colors.purple,
        () {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Settings Coming Soon"),
            ),
          );
        },
      ),
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          "Quick Actions",
          style: TextStyle(
            fontWeight: FontWeight.bold,
            fontSize: 24,
          ),
        ),
        const SizedBox(height: 18),
        desktop
            ? Row(
                children: actions
                    .map(
                      (e) => Expanded(
                        child: Padding(
                          padding: const EdgeInsets.all(8),
                          child: e,
                        ),
                      ),
                    )
                    .toList(),
              )
            : Column(children: actions),
      ],
    );
  }

  Widget _actionButton(
    BuildContext context,
    String title,
    IconData icon,
    Color color,
    VoidCallback onTap,
  ) {
    return SizedBox(
      height: 110,
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.white,
          foregroundColor: Colors.black87,
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(20),
          ),
        ),
        onPressed: onTap,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 34,
              color: color,
            ),
            const SizedBox(height: 10),
            Text(
              title,
              style: const TextStyle(
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ),
    ).animate().fadeIn();
  }

  Widget _buildAIInsights() {
    return Card(
      elevation: 3,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(22),
      ),
      child: const Padding(
        padding: EdgeInsets.all(25),
        child: Row(
          children: [
            CircleAvatar(
              radius: 34,
              backgroundColor: Color(0xff2563EB),
              child: Icon(
                Icons.smart_toy,
                color: Colors.white,
                size: 34,
              ),
            ),
            SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "AI Insight",
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      fontSize: 20,
                    ),
                  ),
                  SizedBox(height: 10),
                  Text(
                    "Twin Engine analytics will appear here after result processing.",
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    ).animate().fadeIn(delay: 400.ms);
  }
}