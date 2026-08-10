from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Flutter",
        "slug": "introduction",
        "order": 1,
        "summary": "Google's toolkit for building one app that runs on mobile, web, and desktop.",
        "body": """
<p>Flutter is a UI toolkit, written in Dart, for building natively-compiled apps from a
single codebase &mdash; the same code can ship to iOS, Android, web, and desktop. Instead of
dragging elements in a visual designer, you describe your UI in code as a tree of
<strong>widgets</strong>, and Flutter draws it. <code>runApp()</code> is the entry point that
starts a Flutter app.</p>
""",
        "example_code": """import 'package:flutter/material.dart';

void main() {
  runApp(
    const Center(
      child: Text('Hello, Flutter!', textDirection: TextDirection.ltr),
    ),
  );
}""",
        "expected_output": "Renders a single line of centered text reading \"Hello, Flutter!\".",
    },
    {
        "title": "Widgets — The Building Blocks",
        "slug": "widgets",
        "order": 2,
        "summary": "Everything in a Flutter UI is a widget, nested inside other widgets.",
        "body": """
<p>In Flutter, <em>everything</em> is a widget &mdash; text, buttons, padding, even layout
itself. You build a screen by nesting widgets inside each other's <code>child</code> (or
<code>children</code>) property, forming a tree. Flutter re-draws only the parts of that
tree that actually changed, which is part of why it's fast.</p>
""",
        "example_code": """Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: const Text('My App')),
    body: const Padding(
      padding: EdgeInsets.all(16.0),
      child: Text('Welcome to my first screen!'),
    ),
  );
}""",
        "expected_output": "Renders a screen with a top app bar titled \"My App\", and padded body text below it.",
    },
    {
        "title": "StatelessWidget",
        "slug": "statelesswidget",
        "order": 3,
        "summary": "A widget that never changes once built.",
        "body": """
<p>A <code>StatelessWidget</code> describes UI that doesn't change over time &mdash; given
the same inputs, it always looks the same. You define it as a class extending
<code>StatelessWidget</code>, and override its <code>build()</code> method to return the
widget tree.</p>
""",
        "example_code": """class GreetingCard extends StatelessWidget {
  final String name;
  const GreetingCard({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}""",
        "expected_output": "Defines a reusable widget that displays \"Hello, {name}!\" — e.g. GreetingCard(name: 'Ada') renders \"Hello, Ada!\".",
    },
    {
        "title": "StatefulWidget & setState",
        "slug": "statefulwidget",
        "order": 4,
        "summary": "A widget that can change itself in response to interaction.",
        "body": """
<p>A <code>StatefulWidget</code> can redraw itself when its data changes &mdash; a counter
that goes up on tap, for example. It's split into two classes: the widget itself, and a
matching <code>State</code> class holding the mutable data. Calling <code>setState()</code>
tells Flutter "something changed, please rebuild this widget."</p>
""",
        "example_code": """class Counter extends StatefulWidget {
  const Counter({super.key});
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => setState(() => count++),
          child: const Text('Add'),
        ),
      ],
    );
  }
}""",
        "expected_output": "Renders \"Count: 0\" with an \"Add\" button beneath it; each tap increments the displayed count by 1.",
    },
    {
        "title": "Layout with Row, Column & Container",
        "slug": "layout",
        "order": 5,
        "summary": "Arranging widgets horizontally, vertically, and with spacing.",
        "body": """
<p><code>Row</code> arranges its children left-to-right; <code>Column</code> arranges them
top-to-bottom. <code>Container</code> wraps a single child to add padding, margin, size, or
a background color &mdash; it's the Flutter equivalent of a styled <code>&lt;div&gt;</code>.</p>
""",
        "example_code": """Widget build(BuildContext context) {
  return Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      Container(color: Colors.blue, width: 50, height: 50),
      Container(color: Colors.orange, width: 50, height: 50),
      Container(color: Colors.green, width: 50, height: 50),
    ],
  );
}""",
        "expected_output": "Renders three evenly-spaced colored squares (blue, orange, green) in a horizontal row.",
    },
    {
        "title": "Handling User Input",
        "slug": "user-input",
        "order": 6,
        "summary": "Buttons and text fields, and reacting to what the user does.",
        "body": """
<p><code>ElevatedButton</code>'s <code>onPressed</code> runs a function when tapped.
<code>TextField</code> collects typed text, usually paired with a
<code>TextEditingController</code> so your code can read what was typed.</p>
""",
        "example_code": """final controller = TextEditingController();

Widget build(BuildContext context) {
  return Column(
    children: [
      TextField(controller: controller),
      ElevatedButton(
        onPressed: () => print('You typed: ${controller.text}'),
        child: const Text('Submit'),
      ),
    ],
  );
}""",
        "expected_output": "Renders a text input above a \"Submit\" button; tapping Submit prints whatever was typed into the field.",
    },
    {
        "title": "Styling Widgets",
        "slug": "styling",
        "order": 7,
        "summary": "TextStyle, colors, and rounded corners.",
        "body": """
<p>Most widgets accept a <code>style</code> parameter. <code>Text</code> takes a
<code>TextStyle</code> (font size, weight, color); <code>Container</code> takes a
<code>BoxDecoration</code> for things like rounded corners and background color.</p>
""",
        "example_code": """Widget build(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.blue,
      borderRadius: BorderRadius.circular(12),
    ),
    child: const Text(
      'Styled box',
      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
    ),
  );
}""",
        "expected_output": "Renders a blue box with rounded corners containing bold, white, 18px text reading \"Styled box\".",
    },
    {
        "title": "Navigating Between Screens",
        "slug": "navigation",
        "order": 8,
        "summary": "Pushing a new screen onto the stack with Navigator.",
        "body": """
<p>Flutter treats screens as a stack. <code>Navigator.push()</code> adds a new screen on
top (with a <code>MaterialPageRoute</code> wrapping the widget to show), and
<code>Navigator.pop()</code> removes the current screen to go back to the previous one.</p>
""",
        "example_code": """ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SecondScreen()),
    );
  },
  child: const Text('Go to Second Screen'),
)""",
        "expected_output": "Tapping the button pushes a new screen (SecondScreen) on top of the current one; a system back gesture or Navigator.pop() returns to this screen.",
    },
]


def seed_flutter_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="flutter",
        defaults={
            "name": "Flutter",
            "icon": "\U0001F4F1",
            "description": "Google's UI toolkit for building one app that runs on mobile, web, and desktop.",
            "editor_language": "flutter",
            "order": 11,
            "is_active": True,
        },
    )

    for data in ARTICLES:
        Article.objects.update_or_create(
            subject=subject,
            slug=data["slug"],
            defaults={
                "title": data["title"],
                "order": data["order"],
                "summary": data["summary"],
                "body": data["body"],
                "example_code": data["example_code"],
                "expected_output": data["expected_output"],
            },
        )


def unseed_flutter_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="flutter").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0013_seed_dart_subject"),
    ]

    operations = [
        migrations.RunPython(seed_flutter_subject, unseed_flutter_subject),
    ]
