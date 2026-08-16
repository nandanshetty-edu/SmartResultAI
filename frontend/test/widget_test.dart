import 'package:flutter_test/flutter_test.dart';

import 'package:smart_result_ai/main.dart';

void main() {
  testWidgets(
    'SmartResult AI app loads',
    (WidgetTester tester) async {
      await tester.pumpWidget(
        const SmartResultAI(),
      );

      await tester.pump();

      expect(
        find.text('SmartResult AI'),
        findsOneWidget,
      );
    },
  );
}