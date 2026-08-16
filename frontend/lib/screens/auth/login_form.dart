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
  State<LoginForm> createState() =>
      _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey =
      GlobalKey<FormState>();

  final _emailController =
      TextEditingController();

  final _passwordController =
      TextEditingController();

  bool obscurePassword = true;

  bool rememberMe = false;

  bool loading = false;

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();

    super.dispose();
  }

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
      final response =
          await AuthService.login(
        email: _emailController.text,
        password: _passwordController.text,
      );

      if (!mounted) return;

      if (widget.onLogin != null) {
        await widget.onLogin!(
          response,
        );
      }
    } catch (e) {
      if (!mounted) return;

      final message =
          e.toString().replaceFirst(
                "Exception: ",
                "",
              );

      ScaffoldMessenger.of(context)
          .showSnackBar(
        SnackBar(
          content: Text(message),
          behavior:
              SnackBarBehavior.floating,
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

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,

      child: Column(
        crossAxisAlignment:
            CrossAxisAlignment.stretch,

        children: [
          Text(
            "Welcome Back 👋",

            style: Theme.of(context)
                .textTheme
                .headlineSmall
                ?.copyWith(
                  fontWeight:
                      FontWeight.bold,
                ),
          ),

          const SizedBox(height: 8),

          Text(
            "Login to continue",

            style: TextStyle(
              color: Colors.grey.shade600,
            ),
          ),

          const SizedBox(height: 30),

          TextFormField(
            controller:
                _emailController,

            keyboardType:
                TextInputType.emailAddress,

            textInputAction:
                TextInputAction.next,

            decoration:
                const InputDecoration(
              labelText: "Email",

              prefixIcon: Icon(
                Icons.email_outlined,
              ),
            ),

            validator: (value) {
              if (value == null ||
                  value.trim().isEmpty) {
                return "Email is required";
              }

              if (!value.contains("@")) {
                return "Enter a valid email";
              }

              return null;
            },
          ),

          const SizedBox(height: 20),

          TextFormField(
            controller:
                _passwordController,

            obscureText:
                obscurePassword,

            textInputAction:
                TextInputAction.done,

            onFieldSubmitted: (_) {
              login();
            },

            decoration:
                InputDecoration(
              labelText: "Password",

              prefixIcon:
                  const Icon(
                Icons.lock_outline,
              ),

              suffixIcon:
                  IconButton(
                onPressed: () {
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

          Row(
            children: [
              Checkbox(
                value: rememberMe,

                onChanged:
                    loading
                        ? null
                        : (value) {
                            setState(() {
                              rememberMe =
                                  value ??
                                      false;
                            });
                          },
              ),

              const Text(
                "Remember Me",
              ),
            ],
          ),

          const SizedBox(height: 25),

          SizedBox(
            height: 55,

            child:
                ElevatedButton(
              onPressed:
                  loading
                      ? null
                      : login,

              child:
                  loading
                      ? const SizedBox(
                          width: 24,
                          height: 24,

                          child:
                              CircularProgressIndicator(
                            strokeWidth: 2.5,
                            color:
                                Colors.white,
                          ),
                        )
                      : const Text(
                          "LOGIN",

                          style:
                              TextStyle(
                            fontSize: 16,
                            fontWeight:
                                FontWeight.w600,
                          ),
                        ),
            ),
          ),

          const SizedBox(height: 20),

          const Divider(),

          const SizedBox(height: 10),

          Center(
            child: Text(
              "MIT Kundapura",

              style: TextStyle(
                color:
                    Colors.grey.shade700,
              ),
            ),
          ),

          const SizedBox(height: 5),

          Center(
            child: Text(
              "Version 1.0",

              style: TextStyle(
                color:
                    Colors.grey.shade500,

                fontSize: 12,
              ),
            ),
          ),
        ],
      ),
    );
  }
}