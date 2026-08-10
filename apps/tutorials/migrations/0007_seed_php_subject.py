from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to PHP",
        "slug": "introduction",
        "order": 1,
        "summary": "A server-side language that runs before the page reaches the browser.",
        "body": """
<p>PHP runs on the server, not in the browser &mdash; it generates HTML which then gets sent
to the visitor. It powers a huge share of the web (WordPress, for one). PHP code lives
between <code>&lt;?php</code> and <code>?&gt;</code> tags, and statements end with a
semicolon. <code>echo</code> outputs text.</p>
""",
        "example_code": '<?php\n  echo "Hello, world!";\n?>',
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables",
        "slug": "variables",
        "order": 2,
        "summary": "PHP variables always start with a dollar sign.",
        "body": """
<p>Every PHP variable name starts with <code>$</code>: <code>$name = "Ada";</code>. Like
Python, you don't declare a type &mdash; it's inferred from the value you assign.</p>
""",
        "example_code": '<?php\n  $name = "Ada";\n  $age = 21;\n  echo "$name is $age years old.";\n?>',
        "expected_output": "Ada is 21 years old.",
    },
    {
        "title": "Echo & String Concatenation",
        "slug": "echo-and-concatenation",
        "order": 3,
        "summary": "Joining strings together with the dot operator.",
        "body": """
<p><code>echo</code> can print several things separated by commas, or you can join
(<strong>concatenate</strong>) strings into one with the <code>.</code> operator.</p>
""",
        "example_code": '<?php\n  $first = "Chi";\n  $last = "nedu";\n  echo $first . $last;\n?>',
        "expected_output": "Chinedu",
    },
    {
        "title": "Operators",
        "slug": "operators",
        "order": 4,
        "summary": "Arithmetic, comparison, and logical operators.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison (<code>== != &gt; &lt;</code>, or
<code>===</code> for a stricter type-aware comparison), and logical
(<code>&& || !</code>) operators all work much like in JavaScript.</p>
""",
        "example_code": '<?php\n  $score = 85;\n  $passed = $score >= 50 && $score <= 100;\n  echo $passed ? "true" : "false";\n?>',
        "expected_output": "true",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 5,
        "summary": "Branching with if, elseif, and else.",
        "body": """
<p><code>if</code>, <code>elseif</code>, and <code>else</code> work the same as most
C-family languages &mdash; each block is wrapped in curly braces.</p>
""",
        "example_code": '<?php\n  $hour = 14;\n\n  if ($hour < 12) {\n    echo "Good morning";\n  } elseif ($hour < 18) {\n    echo "Good afternoon";\n  } else {\n    echo "Good evening";\n  }\n?>',
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 6,
        "summary": "Repeating code with for, while, and foreach.",
        "body": """
<p><code>for</code> and <code>while</code> loops work like most C-family languages.
<code>foreach</code> is PHP's dedicated way to step through every item in an array without
managing an index yourself.</p>
""",
        "example_code": '<?php\n  $total = 0;\n  for ($i = 1; $i <= 5; $i++) {\n    $total += $i;\n  }\n  echo "Total: $total";\n?>',
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 7,
        "summary": "Defining reusable logic with the function keyword.",
        "body": """
<p>Define a function with <code>function name($params) { ... }</code>, and
<code>return</code> a value if it should produce one.</p>
""",
        "example_code": '<?php\n  function greet($name) {\n    return "Hello, $name!";\n  }\n\n  echo greet("Chidi");\n?>',
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Arrays",
        "slug": "arrays",
        "order": 8,
        "summary": "Indexed and associative arrays.",
        "body": """
<p>A regular (indexed) array is a numbered list: <code>$fruits = ["apple", "banana"]</code>.
An <strong>associative</strong> array uses named keys instead of numbers:
<code>$student = ["name" =&gt; "Ada", "track" =&gt; "Frontend"]</code>.
<code>foreach</code> steps through either kind.</p>
""",
        "example_code": '<?php\n  $student = ["name" => "Ada", "track" => "Frontend"];\n  echo $student["name"] . " is studying " . $student["track"];\n?>',
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_php_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="php",
        defaults={
            "name": "PHP",
            "icon": "\U0001F418",
            "description": "A server-side scripting language that powers a huge share of the web.",
            "editor_language": "php",
            "order": 5,
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


def unseed_php_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="php").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0006_seed_python_subject"),
    ]

    operations = [
        migrations.RunPython(seed_php_subject, unseed_php_subject),
    ]
