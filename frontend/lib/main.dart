import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'core/theme/app_theme.dart';
import 'screens/splash/splash_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  runApp(
    const ProviderScope(
      child: SmartResultAI(),
    ),
  );
}

class SmartResultAI extends StatelessWidget {
  const SmartResultAI({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SmartResult AI',

      debugShowCheckedModeBanner: false,

      theme: AppTheme.lightTheme,

      darkTheme: AppTheme.darkTheme,

      themeMode: ThemeMode.system,

      home: const SplashScreen(),
    );
  }
}