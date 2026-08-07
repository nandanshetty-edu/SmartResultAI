import 'package:flutter/material.dart';

class LoginForm extends StatefulWidget {
  final VoidCallback? onLogin;

  const LoginForm({
    super.key,
    this.onLogin,
  });

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {

  final _formKey = GlobalKey<FormState>();

  final _emailController = TextEditingController();

  final _passwordController = TextEditingController();

  bool obscurePassword = true;

  bool rememberMe = false;

  @override
  void dispose() {

    _emailController.dispose();

    _passwordController.dispose();

    super.dispose();
  }

  void login() {

    if (!_formKey.currentState!.validate()) {

      return;

    }

    if (widget.onLogin != null) {

      widget.onLogin!();

    } else {

      ScaffoldMessenger.of(context).showSnackBar(

        const SnackBar(

          content: Text(
            "Backend login will be connected next.",
          ),

        ),

      );

    }

  }

  @override
  Widget build(BuildContext context) {

    return Form(

      key: _formKey,

      child: Column(

        crossAxisAlignment: CrossAxisAlignment.stretch,

        children: [

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

          const SizedBox(height: 30),

          TextFormField(

            controller: _emailController,

            keyboardType: TextInputType.emailAddress,

            decoration: const InputDecoration(

              labelText: "College Email",

              prefixIcon: Icon(Icons.email_outlined),

            ),

            validator: (value) {

              if (value == null || value.isEmpty) {

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

            controller: _passwordController,

            obscureText: obscurePassword,

            decoration: InputDecoration(

              labelText: "Password",

              prefixIcon: const Icon(Icons.lock_outline),

              suffixIcon: IconButton(

                onPressed: () {

                  setState(() {

                    obscurePassword = !obscurePassword;

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

              if (value == null || value.isEmpty) {

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

                onChanged: (value) {

                  setState(() {

                    rememberMe = value ?? false;

                  });

                },

              ),

              const Text("Remember Me"),

            ],

          ),

          const SizedBox(height: 25),

          SizedBox(

            height: 55,

            child: ElevatedButton(

              onPressed: login,

              child: const Text(

                "LOGIN",

                style: TextStyle(
                  fontSize: 16,
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