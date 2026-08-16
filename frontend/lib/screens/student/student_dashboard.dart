import 'package:flutter/material.dart';
import 'package:flutter_animate/flutter_animate.dart';

import '../../services/auth_service.dart';
import '../../services/student_service.dart';

class StudentDashboard extends StatefulWidget {
  const StudentDashboard({
    super.key,
  });

  @override
  State<StudentDashboard> createState() =>
      _StudentDashboardState();
}

class _StudentDashboardState
    extends State<StudentDashboard> {
  Map<String, dynamic>? student;

  List<Map<String, dynamic>> results = [];

  bool loading = true;

  String? errorMessage;

  @override
  void initState() {
    super.initState();

    loadDashboard();
  }

  Future<void> loadDashboard() async {
    setState(() {
      loading = true;
      errorMessage = null;
    });

    try {
      final profile =
          await StudentService.getProfile();

      final studentResults =
          await StudentService.getResults();

      if (!mounted) return;

      setState(() {
        student = profile;
        results = studentResults;
        loading = false;
      });
    } catch (e) {
      if (!mounted) return;

      setState(() {
        loading = false;
        errorMessage = e
            .toString()
            .replaceFirst(
              "Exception: ",
              "",
            );
      });
    }
  }

  Future<void> logout() async {
    await AuthService.logout();

    if (!mounted) return;

    Navigator.of(context).popUntil(
      (route) => route.isFirst,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor:
          const Color(0xffF8FAFC),

      appBar: AppBar(
        elevation: 0,

        backgroundColor:
            Colors.transparent,

        title: const Text(
          "My Results",
          style: TextStyle(
            fontWeight:
                FontWeight.bold,
          ),
        ),

        actions: [
          IconButton(
            tooltip: "Refresh",

            onPressed:
                loading
                    ? null
                    : loadDashboard,

            icon: const Icon(
              Icons.refresh,
            ),
          ),

          IconButton(
            tooltip: "Logout",

            onPressed: logout,

            icon: const Icon(
              Icons.logout,
            ),
          ),

          const SizedBox(width: 10),
        ],
      ),

      body: loading
          ? const Center(
              child:
                  CircularProgressIndicator(),
            )
          : errorMessage != null
              ? _buildError()
              : RefreshIndicator(
                  onRefresh:
                      loadDashboard,

                  child:
                      SingleChildScrollView(
                    physics:
                        const AlwaysScrollableScrollPhysics(),

                    padding:
                        const EdgeInsets.all(
                      24,
                    ),

                    child: Center(
                      child:
                          ConstrainedBox(
                        constraints:
                            const BoxConstraints(
                          maxWidth: 1200,
                        ),

                        child: Column(
                          crossAxisAlignment:
                              CrossAxisAlignment
                                  .start,

                          children: [
                            _buildWelcomeCard(),

                            const SizedBox(
                              height: 25,
                            ),

                            _buildStats(),

                            const SizedBox(
                              height: 25,
                            ),

                            _buildResults(),

                            const SizedBox(
                              height: 25,
                            ),

                            _buildAIInsight(),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
    );
  }

  // ==========================================================
  // ERROR
  // ==========================================================

  Widget _buildError() {
    return Center(
      child: Padding(
        padding:
            const EdgeInsets.all(30),

        child: Column(
          mainAxisSize:
              MainAxisSize.min,

          children: [
            const Icon(
              Icons.cloud_off,
              size: 60,
              color: Colors.red,
            ),

            const SizedBox(
              height: 20,
            ),

            const Text(
              "Unable to load dashboard",

              style: TextStyle(
                fontSize: 20,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            Text(
              errorMessage ??
                  "Unknown error",

              textAlign:
                  TextAlign.center,
            ),

            const SizedBox(
              height: 20,
            ),

            ElevatedButton.icon(
              onPressed:
                  loadDashboard,

              icon: const Icon(
                Icons.refresh,
              ),

              label:
                  const Text(
                "Try Again",
              ),
            ),
          ],
        ),
      ),
    );
  }

  // ==========================================================
  // WELCOME
  // ==========================================================

  Widget _buildWelcomeCard() {
    final name =
        student?["name"] ??
            "Student";

    final usn =
        student?["usn"] ??
            "N/A";

    return Container(
      width: double.infinity,

      padding:
          const EdgeInsets.all(28),

      decoration:
          BoxDecoration(
        gradient:
            const LinearGradient(
          colors: [
            Color(0xff2563EB),
            Color(0xff4F46E5),
          ],

          begin:
              Alignment.topLeft,

          end:
              Alignment.bottomRight,
        ),

        borderRadius:
            BorderRadius.circular(
          25,
        ),
      ),

      child: Row(
        children: [
          const CircleAvatar(
            radius: 38,

            backgroundColor:
                Colors.white,

            child: Icon(
              Icons.school_rounded,

              color:
                  Color(0xff2563EB),

              size: 42,
            ),
          ),

          const SizedBox(
            width: 20,
          ),

          Expanded(
            child: Column(
              crossAxisAlignment:
                  CrossAxisAlignment.start,

              children: [
                const Text(
                  "Welcome Back 👋",

                  style: TextStyle(
                    color:
                        Colors.white70,

                    fontSize: 17,
                  ),
                ),

                const SizedBox(
                  height: 6,
                ),

                Text(
                  name.toString(),

                  style:
                      const TextStyle(
                    color: Colors.white,

                    fontSize: 28,

                    fontWeight:
                        FontWeight.bold,
                  ),
                ),

                const SizedBox(
                  height: 8,
                ),

                Text(
                  "USN: $usn",

                  style:
                      const TextStyle(
                    color:
                        Colors.white70,

                    fontSize: 15,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    )
        .animate()
        .fadeIn()
        .slideY(
          begin: -.15,
        );
  }

  // ==========================================================
  // STATS
  // ==========================================================

  Widget _buildStats() {
    final cgpa =
        _formatNumber(
      student?["cgpa"],
    );

    final semester =
        student?["semester"]
                ?.toString() ??
            "-";

    final section =
        student?["section"]
                ?.toString() ??
            "-";

    final resultCount =
        results.length.toString();

    return LayoutBuilder(
      builder:
          (context, constraints) {
        final desktop =
            constraints.maxWidth >
                700;

        final cards = [
          _statCard(
            title: "CGPA",
            value: cgpa,
            icon:
                Icons.school_rounded,
            color:
                Colors.blue,
          ),

          _statCard(
            title: "Results",
            value: resultCount,
            icon:
                Icons.assignment_turned_in,
            color:
                Colors.green,
          ),

          _statCard(
            title: "Semester",
            value: semester,
            icon:
                Icons.calendar_month,
            color:
                Colors.orange,
          ),

          _statCard(
            title: "Section",
            value: section,
            icon:
                Icons.groups,
            color:
                Colors.purple,
          ),
        ];

        if (desktop) {
          return Row(
            children:
                cards.map(
              (card) {
                return Expanded(
                  child: Padding(
                    padding:
                        const EdgeInsets.all(
                      7,
                    ),

                    child: card,
                  ),
                );
              },
            ).toList(),
          );
        }

        return Column(
          children: cards,
        );
      },
    );
  }

  Widget _statCard({
    required String title,
    required String value,
    required IconData icon,
    required Color color,
  }) {
    return Card(
      elevation: 2,

      shape:
          RoundedRectangleBorder(
        borderRadius:
            BorderRadius.circular(
          20,
        ),
      ),

      child: Padding(
        padding:
            const EdgeInsets.all(22),

        child: Column(
          children: [
            CircleAvatar(
              radius: 27,

              backgroundColor:
                  color.withOpacity(
                .12,
              ),

              child: Icon(
                icon,
                color: color,
              ),
            ),

            const SizedBox(
              height: 15,
            ),

            Text(
              value,

              style:
                  const TextStyle(
                fontSize: 28,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 5,
            ),

            Text(
              title,

              style: TextStyle(
                color:
                    Colors.grey.shade600,
              ),
            ),
          ],
        ),
      ),
    )
        .animate()
        .fadeIn()
        .scale();
  }

  // ==========================================================
  // RESULTS
  // ==========================================================

  Widget _buildResults() {
    return Card(
      elevation: 2,

      shape:
          RoundedRectangleBorder(
        borderRadius:
            BorderRadius.circular(
          22,
        ),
      ),

      child: Padding(
        padding:
            const EdgeInsets.all(25),

        child: Column(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          children: [
            const Text(
              "Semester Results",

              style:
                  TextStyle(
                fontSize: 21,
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 18,
            ),

            if (results.isEmpty)
              _buildEmptyResults()
            else
              ...results.map(
                (result) =>
                    _buildResultCard(
                  result,
                ),
              ),
          ],
        ),
      ),
    )
        .animate()
        .fadeIn(
          delay: 200.ms,
        );
  }

  Widget _buildEmptyResults() {
    return Container(
      width: double.infinity,

      padding:
          const EdgeInsets.all(30),

      decoration:
          BoxDecoration(
        color:
            const Color(
          0xffF8FAFC,
        ),

        borderRadius:
            BorderRadius.circular(
          16,
        ),
      ),

      child: const Column(
        children: [
          Icon(
            Icons
                .assignment_outlined,

            size: 48,

            color:
                Colors.grey,
          ),

          SizedBox(
            height: 12,
          ),

          Text(
            "No published results yet",

            style: TextStyle(
              fontSize: 16,
              fontWeight:
                  FontWeight.w600,
            ),
          ),

          SizedBox(
            height: 6,
          ),

          Text(
            "Your results will appear here once they are published by your college.",

            textAlign:
                TextAlign.center,

            style: TextStyle(
              color: Colors.grey,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildResultCard(
    Map<String, dynamic> result,
  ) {
    final exam =
        result["exam"] is Map
            ? Map<String, dynamic>.from(
                result["exam"],
              )
            : <String, dynamic>{};

    final semester =
        exam["semester"]
                ?.toString() ??
            "-";

    final academicYear =
        exam["academic_year"]
                ?.toString() ??
            "-";

    final examType =
        exam["exam_type"]
                ?.toString() ??
            "-";

    final sgpa =
        _formatNumber(
      result["sgpa"],
    );

    final cgpa =
        _formatNumber(
      result["cgpa"],
    );

    final overall =
        result["overall_result"]
                ?.toString() ??
            "-";

    final marks =
        result["marks"] is List
            ? List<dynamic>.from(
                result["marks"],
              )
            : <dynamic>[];

    return Container(
      margin:
          const EdgeInsets.only(
        bottom: 14,
      ),

      padding:
          const EdgeInsets.all(18),

      decoration:
          BoxDecoration(
        color:
            const Color(
          0xffF8FAFC,
        ),

        borderRadius:
            BorderRadius.circular(
          16,
        ),

        border:
            Border.all(
          color:
              Colors.grey.shade200,
        ),
      ),

      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.start,

        children: [
          Row(
            children: [
              const CircleAvatar(
                radius: 23,

                backgroundColor:
                    Color(
                  0xffE0E7FF,
                ),

                child: Icon(
                  Icons
                      .description_outlined,

                  color:
                      Color(
                    0xff2563EB,
                  ),
                ),
              ),

              const SizedBox(
                width: 14,
              ),

              Expanded(
                child: Column(
                  crossAxisAlignment:
                      CrossAxisAlignment
                          .start,

                  children: [
                    Text(
                      "Semester $semester",

                      style:
                          const TextStyle(
                        fontWeight:
                            FontWeight.bold,

                        fontSize: 17,
                      ),
                    ),

                    const SizedBox(
                      height: 3,
                    ),

                    Text(
                      "$academicYear • $examType",

                      style:
                          TextStyle(
                        color: Colors
                            .grey
                            .shade600,

                        fontSize: 13,
                      ),
                    ),
                  ],
                ),
              ),

              _resultBadge(
                overall,
              ),
            ],
          ),

          const SizedBox(
            height: 18,
          ),

          Row(
            children: [
              Expanded(
                child:
                    _resultStat(
                  "SGPA",
                  sgpa,
                ),
              ),

              Expanded(
                child:
                    _resultStat(
                  "CGPA",
                  cgpa,
                ),
              ),

              Expanded(
                child:
                    _resultStat(
                  "Subjects",
                  marks.length
                      .toString(),
                ),
              ),
            ],
          ),

          if (marks.isNotEmpty) ...[
            const SizedBox(
              height: 20,
            ),

            const Divider(),

            const SizedBox(
              height: 10,
            ),

            const Text(
              "Subjects",

              style:
                  TextStyle(
                fontWeight:
                    FontWeight.bold,
              ),
            ),

            const SizedBox(
              height: 10,
            ),

            ...marks.map(
              (mark) =>
                  _buildMarkRow(
                mark,
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _resultStat(
    String title,
    String value,
  ) {
    return Column(
      children: [
        Text(
          value,

          style:
              const TextStyle(
            fontSize: 20,
            fontWeight:
                FontWeight.bold,
          ),
        ),

        const SizedBox(
          height: 3,
        ),

        Text(
          title,

          style:
              TextStyle(
            fontSize: 12,
            color:
                Colors.grey.shade600,
          ),
        ),
      ],
    );
  }

  Widget _resultBadge(
    String result,
  ) {
    final isPass =
        result.toUpperCase() ==
            "PASS";

    return Container(
      padding:
          const EdgeInsets.symmetric(
        horizontal: 12,
        vertical: 6,
      ),

      decoration:
          BoxDecoration(
        color: isPass
            ? Colors.green
                .withOpacity(.1)
            : Colors.red
                .withOpacity(.1),

        borderRadius:
            BorderRadius.circular(
          20,
        ),
      ),

      child: Text(
        result,

        style:
            TextStyle(
          color: isPass
              ? Colors.green
              : Colors.red,

          fontWeight:
              FontWeight.w600,

          fontSize: 12,
        ),
      ),
    );
  }

  Widget _buildMarkRow(
    dynamic markData,
  ) {
    if (markData is! Map) {
      return const SizedBox();
    }

    final mark =
        Map<String, dynamic>.from(
      markData,
    );

    final code =
        mark["subject_code"]
                ?.toString() ??
            "-";

    final name =
        mark["subject_name"]
                ?.toString() ??
            "Unknown Subject";

    final internal =
        mark["internal"]
                ?.toString() ??
            "-";

    final external =
        mark["external"]
                ?.toString() ??
            "-";

    final total =
        mark["total"]
                ?.toString() ??
            "-";

    final status =
        mark["result"]
                ?.toString() ??
            "-";

    return Padding(
      padding:
          const EdgeInsets.symmetric(
        vertical: 8,
      ),

      child: Row(
        children: [
          SizedBox(
            width: 70,

            child: Text(
              code,

              style:
                  const TextStyle(
                fontWeight:
                    FontWeight.w600,

                fontSize: 12,
              ),
            ),
          ),

          Expanded(
            child: Text(
              name,

              maxLines: 1,

              overflow:
                  TextOverflow.ellipsis,

              style:
                  const TextStyle(
                fontSize: 13,
              ),
            ),
          ),

          _markValue(
            "IA",
            internal,
          ),

          _markValue(
            "SEE",
            external,
          ),

          _markValue(
            "Total",
            total,
          ),

          const SizedBox(
            width: 8,
          ),

          Text(
            status,

            style:
                TextStyle(
              fontSize: 12,

              fontWeight:
                  FontWeight.bold,

              color:
                  status.toUpperCase() ==
                          "PASS"
                      ? Colors.green
                      : Colors.red,
            ),
          ),
        ],
      ),
    );
  }

  Widget _markValue(
    String label,
    String value,
  ) {
    return Padding(
      padding:
          const EdgeInsets.only(
        left: 10,
      ),

      child: Column(
        children: [
          Text(
            value,

            style:
                const TextStyle(
              fontWeight:
                  FontWeight.w600,

              fontSize: 12,
            ),
          ),

          Text(
            label,

            style:
                TextStyle(
              fontSize: 9,
              color:
                  Colors.grey.shade500,
            ),
          ),
        ],
      ),
    );
  }

  // ==========================================================
  // AI INSIGHT
  // ==========================================================

  Widget _buildAIInsight() {
    return Card(
      elevation: 2,

      shape:
          RoundedRectangleBorder(
        borderRadius:
            BorderRadius.circular(
          22,
        ),
      ),

      child: Padding(
        padding:
            const EdgeInsets.all(25),

        child: Row(
          crossAxisAlignment:
              CrossAxisAlignment.start,

          children: [
            const CircleAvatar(
              radius: 30,

              backgroundColor:
                  Color(0xff2563EB),

              child: Icon(
                Icons.smart_toy,

                color:
                    Colors.white,

                size: 30,
              ),
            ),

            const SizedBox(
              width: 18,
            ),

            const Expanded(
              child: Column(
                crossAxisAlignment:
                    CrossAxisAlignment
                        .start,

                children: [
                  Text(
                    "AI Academic Insight",

                    style:
                        TextStyle(
                      fontSize: 19,
                      fontWeight:
                          FontWeight.bold,
                    ),
                  ),

                  SizedBox(
                    height: 8,
                  ),

                  Text(
                    "Personalized performance insights will appear here as your results become available.",
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    )
        .animate()
        .fadeIn(
          delay: 400.ms,
        );
  }

  // ==========================================================
  // HELPERS
  // ==========================================================

  String _formatNumber(
    dynamic value,
  ) {
    if (value == null) {
      return "0.00";
    }

    if (value is num) {
      return value.toStringAsFixed(
        2,
      );
    }

    final parsed =
        double.tryParse(
      value.toString(),
    );

    if (parsed == null) {
      return "0.00";
    }

    return parsed.toStringAsFixed(
      2,
    );
  }
}