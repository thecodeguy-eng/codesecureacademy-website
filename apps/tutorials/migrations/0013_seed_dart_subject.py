from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Dart",
        "slug": "introduction",
        "order": 1,
        "summary": "A client-optimized language from Google, best known as Flutter's language.",
        "body": """
<p>Dart is a language built by Google for building fast apps on any platform &mdash; it's
best known today as the language Flutter apps are written in. Its syntax will feel familiar
if you've used Java, JavaScript, or C#. Every Dart program starts execution from a
<code>main()</code> function, and <code>print()</code> outputs a line of text.</p>
""",
        "example_code": """void main() {
  print('Hello, world!');
}""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "var, final, const, and Dart's core types.",
        "body": """
<p>Declare a variable with <code>var</code> and Dart infers its type from the assigned
value. Use <code>final</code> for a value that's set once and never reassigned, and
<code>const</code> for a compile-time constant. Core types include <code>String</code>,
<code>int</code>, <code>double</code>, and <code>bool</code>.</p>
""",
        "example_code": """void main() {
  String name = 'Ada';
  int age = 21;
  print('$name is $age years old.');
}""",
        "expected_output": "Ada is 21 years old.",
    },
    {
        "title": "Operators",
        "slug": "operators",
        "order": 3,
        "summary": "Arithmetic, comparison, and logical operators.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison (<code>== != &gt; &lt;</code>), and
logical (<code>&& || !</code>) operators all work as you'd expect from other
C-family languages.</p>
""",
        "example_code": """void main() {
  int score = 85;
  bool passed = score >= 50 && score <= 100;
  print('Passed: $passed');
}""",
        "expected_output": "Passed: true",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 4,
        "summary": "Branching with if, else if, and else.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work the same as in Java,
JavaScript, or C#.</p>
""",
        "example_code": """void main() {
  int hour = 14;
  String greeting;

  if (hour < 12) {
    greeting = 'Good morning';
  } else if (hour < 18) {
    greeting = 'Good afternoon';
  } else {
    greeting = 'Good evening';
  }

  print(greeting);
}""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 5,
        "summary": "Repeating code with for and while.",
        "body": """
<p>Dart's <code>for</code> loop uses the familiar three-part structure. There's also a
<code>for-in</code> form for stepping through every item in a list without managing an
index yourself.</p>
""",
        "example_code": """void main() {
  var total = 0;
  for (var i = 1; i <= 5; i++) {
    total += i;
  }
  print('Total: $total');
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 6,
        "summary": "Reusable blocks of code, with an optional return type.",
        "body": """
<p>Define a function with a return type, name, and parameters:
<code>String greet(String name) { ... }</code>. Dart also supports a short arrow syntax
for one-line functions: <code>int square(int n) =&gt; n * n;</code>.</p>
""",
        "example_code": """String greet(String name) {
  return 'Hello, $name!';
}

void main() {
  print(greet('Chidi'));
}""",
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Lists",
        "slug": "lists",
        "order": 7,
        "summary": "Ordered collections, similar to arrays in other languages.",
        "body": """
<p>A <code>List</code> holds an ordered collection of values:
<code>var numbers = [1, 2, 3, 4, 5];</code>. Access items by zero-based index, and use
methods like <code>.map()</code> to transform every item into a new list.</p>
""",
        "example_code": """void main() {
  var numbers = [1, 2, 3, 4, 5];
  var doubled = numbers.map((n) => n * 2).toList();
  print(doubled);
}""",
        "expected_output": "[2, 4, 6, 8, 10]",
    },
    {
        "title": "Classes & Objects",
        "slug": "classes-and-objects",
        "order": 8,
        "summary": "Blueprints (classes) and the instances made from them (objects).",
        "body": """
<p>A class describes fields and methods; <code>ClassName(...)</code> creates an object
from it (Dart doesn't require the <code>new</code> keyword, unlike Java or C#). This same
pattern is exactly how Flutter widgets are built, which is why learning Dart's classes
first makes Flutter much easier to pick up.</p>
""",
        "example_code": """class Student {
  String name;
  String track;

  Student(this.name, this.track);
}

void main() {
  var ada = Student('Ada', 'Frontend');
  print('${ada.name} is studying ${ada.track}');
}""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_dart_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="dart",
        defaults={
            "name": "Dart",
            "icon": "\U0001F3AF",
            "description": "A client-optimized language from Google — best known as the language behind Flutter.",
            "editor_language": "dart",
            "order": 10,
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


def unseed_dart_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="dart").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0012_alter_subject_editor_language"),
    ]

    operations = [
        migrations.RunPython(seed_dart_subject, unseed_dart_subject),
    ]
