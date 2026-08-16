import 'package:flutter/material.dart';

import '../../services/auth_service.dart';

class LoginForm extends StatefulWidget {
  final Future<void> Function(
    Map<String, dynamic> response,
  )? onLogin;

  const LoginForm({
    super.key,
    this.onLogin,
  });

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();

  final _loginController = TextEditingController();
  final _passwordController = TextEditingController();

  bool obscurePassword = true;
  bool rememberMe = false;
  bool loading = false;

  // true  = Student
  // false = Teacher
  bool isStudent = true;

  @override
  void dispose() {
    _loginController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  // ============================================================
  // LOGIN
  // ============================================================

  Future<void> login() async {
    if (!_formKey.currentState!.validate()) {
      return;
    }

    if (loading) {
      return;
    }

    setState(() {
      loading = true;
    });

    try {
      late final Map<String, dynamic> response;

      // --------------------------------------------------------
      // STUDENT
      // --------------------------------------------------------

      if (isStudent) {
        response = await AuthService.loginStudent(
          usn: _loginController.text,
          password: _passwordController.text,
        );
      }

      // --------------------------------------------------------
      // TEACHER
      // --------------------------------------------------------

      else {
        response = await AuthService.loginTeacher(
          email: _loginController.text,
          password: _passwordController.text,
        );
      }

      if (!mounted) return;

      if (widget.onLogin != null) {
        await widget.onLogin!(response);
      }
    } catch (e) {
      if (!mounted) return;

      final message = e.toString().replaceFirst(
        "Exception: ",
        "",
      );

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          behavior: SnackBarBehavior.floating,
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          loading = false;
        });
      }
    }
  }

  // ============================================================
  // ROLE SWITCH
  // ============================================================

  void selectRole(bool student) {
    if (loading) return;

    setState(() {
      isStudent = student;

      // Clear the field when changing role.
      _loginController.clear();

      _formKey.currentState?.reset();
    });
  }

  // ============================================================
  // BUILD
  // ============================================================

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // ======================================================
          // TITLE
          // ======================================================

          Text(
            "Welcome Back 👋",
            style: Theme.of(context)
                .textTheme
                .headlineSmall
                ?.copyWith(
                  fontWeight: FontWeight.bold,
                ),
          ),

          const SizedBox(height: 8),

          Text(
            "Login to continue",
            style: TextStyle(
              color: Colors.grey.shade600,
            ),
          ),

          const SizedBox(height: 25),

          // ======================================================
          // ROLE SELECTOR
          // ======================================================

          Container(
            padding: const EdgeInsets.all(4),
            decoration: BoxDecoration(
              color: Colors.grey.shade200,
              borderRadius: BorderRadius.circular(14),
            ),
            child: Row(
              children: [
                Expanded(
                  child: _RoleButton(
                    title: "Student",
                    icon: Icons.school_outlined,
                    selected: isStudent,
                    onTap: () => selectRole(true),
                  ),
                ),
                Expanded(
                  child: _RoleButton(
                    title: "Teacher",
                    icon: Icons.person_outline,
                    selected: !isStudent,
                    onTap: () => selectRole(false),
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 25),

          // ======================================================
          // LOGIN ID
          // ======================================================

          TextFormField(
            controller: _loginController,
            keyboardType: isStudent
                ? TextInputType.text
                : TextInputType.emailAddress,
            textInputAction: TextInputAction.next,
            textCapitalization: isStudent
                ? TextCapitalization.characters
                : TextCapitalization.none,
            decoration: InputDecoration(
              labelText: isStudent
                  ? "USN"
                  : "College Gmail",
              hintText: isStudent
                  ? "Enter your USN"
                  : "Enter your college Gmail",
              prefixIcon: Icon(
                isStudent
                    ? Icons.badge_outlined
                    : Icons.email_outlined,
              ),
              border: const OutlineInputBorder(),
            ),
            validator: (value) {
              final input = value?.trim() ?? "";

              if (input.isEmpty) {
                return isStudent
                    ? "USN is required"
                    : "College Gmail is required";
              }

              // --------------------------------------------------
              // Student validation
              // --------------------------------------------------

              if (isStudent) {
                if (input.length < 3) {
                  return "Enter a valid USN";
                }

                return null;
              }

              // --------------------------------------------------
              // Teacher validation
              // --------------------------------------------------

              if (!input.contains("@")) {
                return "Enter a valid college Gmail";
              }

              return null;
            },
          ),

          const SizedBox(height: 20),

          // ======================================================
          // PASSWORD
          // ======================================================

          TextFormField(
            controller: _passwordController,
            obscureText: obscurePassword,
            textInputAction: TextInputAction.done,
            onFieldSubmitted: (_) {
              login();
            },
            decoration: InputDecoration(
              labelText: "Password",
              prefixIcon: const Icon(
                Icons.lock_outline,
              ),
              border: const OutlineInputBorder(),
              suffixIcon: IconButton(
                onPressed: loading
                    ? null
                    : () {
                        setState(() {
                          obscurePassword =
                              !obscurePassword;
                        });
                      },
                icon: Icon(
                  obscurePassword
                      ? Icons.visibility
                      : Icons.visibility_off,
                ),
              ),
            ),
            validator: (value) {
              if (value == null ||
                  value.isEmpty) {
                return "Password is required";
              }

              if (value.length < 6) {
                return "Minimum 6 characters";
              }

              return null;
            },
          ),

          const SizedBox(height: 15),

          // ======================================================
          // REMEMBER ME
          // ======================================================

          Row(
            children: [
              Checkbox(
                value: rememberMe,
                onChanged: loading
                    ? null
                    : (value) {
                        setState(() {
                          rememberMe =
                              value ?? false;
                        });
                      },
              ),
              const Text("Remember Me"),
            ],
          ),

          const SizedBox(height: 25),

          // ======================================================
          // LOGIN BUTTON
          // ======================================================

          SizedBox(
            height: 55,
            child: ElevatedButton(
              onPressed: loading ? null : login,
              child: loading
                  ? const SizedBox(
                      width: 24,
                      height: 24,
                      child: CircularProgressIndicator(
                        strokeWidth: 2.5,
                        color: Colors.white,
                      ),
                    )
                  : Text(
                      isStudent
                          ? "LOGIN AS STUDENT"
                          : "LOGIN AS TEACHER",
                      style: const TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w600,
                      ),
                    ),
            ),
          ),

          const SizedBox(height: 20),

          const Divider(),

          const SizedBox(height: 10),

          // ======================================================
          // COLLEGE
          // ======================================================

          Center(
            child: Text(
              "MIT Kundapura",
              style: TextStyle(
                color: Colors.grey.shade700,
              ),
            ),
          ),

          const SizedBox(height: 5),

          Center(
            child: Text(
              "Version 1.0",
              style: TextStyle(
                color: Colors.grey.shade500,
                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }
}

// ================================================================
// ROLE BUTTON
// ================================================================

class _RoleButton extends StatelessWidget {
  final String title;
  final IconData icon;
  final bool selected;
  final VoidCallback onTap;

  const _RoleButton({
    required this.title,
    required this.icon,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: AnimatedContainer(
        duration: const Duration(
          milliseconds: 200,
        ),
        padding: const EdgeInsets.symmetric(
          vertical: 13,
        ),
        decoration: BoxDecoration(
          color: selected
              ? Colors.white
              : Colors.transparent,
          borderRadius: BorderRadius.circular(11),
          boxShadow: selected
              ? [
                  BoxShadow(
                    blurRadius: 6,
                    offset: const Offset(0, 2),
                    color: Colors.black.withValues(
                      alpha: 0.08,
                    ),
                  ),
                ]
              : null,
        ),
        child: Row(
          mainAxisAlignment:
              MainAxisAlignment.center,
          children: [
            Icon(
              icon,
              size: 20,
              color: selected
                  ? const Color(0xff2563EB)
                  : Colors.grey.shade600,
            ),
            const SizedBox(width: 8),
            Text(
              title,
              style: TextStyle(
                fontWeight: selected
                    ? FontWeight.w600
                    : FontWeight.normal,
                color: selected
                    ? const Color(0xff2563EB)
                    : Colors.grey.shade700,
              ),
            ),
          ],
        ),
      ),
    );
  }
}