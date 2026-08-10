from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Python",
        "slug": "introduction",
        "order": 1,
        "summary": "Why Python reads almost like plain English, and how to print output.",
        "body": """
<p>Python is a general-purpose programming language known for clean, readable syntax &mdash;
it uses indentation instead of curly braces to mark blocks of code, which forces consistent
formatting. It's a popular first language, and widely used for web backends, data science,
and automation.</p>
<p><code>print()</code> outputs a value. These examples are read-only here (no in-browser
Python execution), but the expected output is shown below each one so you can follow along.</p>
""",
        "example_code": 'print("Hello, world!")',
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "Assigning values, and Python's core types: str, int, float, bool.",
        "body": """
<p>Python variables don't need a declared type &mdash; just assign a value with
<code>=</code> and Python figures out the type. The core built-in types are
<code>str</code> (text), <code>int</code> (whole numbers), <code>float</code> (decimals),
and <code>bool</code> (<code>True</code>/<code>False</code>). <code>type()</code> tells you
a value's type.</p>
""",
        "example_code": """name = "Ada"
age = 21
gpa = 3.8

print(type(name), type(age), type(gpa))""",
        "expected_output": "<class 'str'> <class 'int'> <class 'float'>",
    },
    {
        "title": "Operators",
        "slug": "operators",
        "order": 3,
        "summary": "Arithmetic, comparison, and logical operators.",
        "body": """
<p>Arithmetic operators (<code>+ - * /</code>) do math, and <code>//</code> and
<code>%</code> give integer division and remainder. Comparison operators
(<code>== != &gt; &lt;</code>) produce a boolean. Logical operators are spelled out as words:
<code>and</code>, <code>or</code>, <code>not</code>.</p>
""",
        "example_code": """score = 85
passed = score >= 50 and score <= 100
print("Passed:", passed)""",
        "expected_output": "Passed: True",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 4,
        "summary": "Branching with if, elif, and else.",
        "body": """
<p><code>if</code> runs a block only when its condition is true. <code>elif</code>
("else if") checks another condition if the first was false, and <code>else</code> catches
everything else. Python uses indentation (not braces) to mark which lines belong to which
block.</p>
""",
        "example_code": """hour = 14

if hour < 12:
    greeting = "Good morning"
elif hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

print(greeting)""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 5,
        "summary": "Repeating code with for and while.",
        "body": """
<p>A <code>for</code> loop steps through a sequence &mdash; often the result of
<code>range(n)</code>, which produces the numbers 0 up to (not including) <code>n</code>.
A <code>while</code> loop repeats as long as its condition stays true.</p>
""",
        "example_code": """total = 0
for i in range(1, 6):
    total += i

print("Total:", total)""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 6,
        "summary": "Defining reusable logic with def.",
        "body": """
<p>Define a function with <code>def name(parameters):</code>, followed by an indented
block, and <code>return</code> a value if the function should produce one. Call it by
name with whatever arguments it needs.</p>
""",
        "example_code": """def greet(name):
    return f"Hello, {name}!"

print(greet("Chidi"))""",
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Lists",
        "slug": "lists",
        "order": 7,
        "summary": "Ordered, changeable collections in square brackets.",
        "body": """
<p>A list holds an ordered collection of values: <code>fruits = ["apple", "banana"]</code>.
Access items by zero-based index (<code>fruits[0]</code>), add with <code>.append()</code>,
and loop over every item with a <code>for</code> loop.</p>
""",
        "example_code": """numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]

print(doubled)""",
        "expected_output": "[2, 4, 6, 8, 10]",
    },
    {
        "title": "Dictionaries",
        "slug": "dictionaries",
        "order": 8,
        "summary": "Key/value pairs for grouping related data.",
        "body": """
<p>A dictionary groups values under named keys:
<code>student = {"name": "Ada", "track": "Frontend"}</code>. Access a value with
<code>student["name"]</code>, or safely with <code>student.get("name")</code>, which
returns <code>None</code> instead of an error if the key doesn't exist.</p>
""",
        "example_code": """student = {"name": "Ada", "track": "Frontend"}
print(student["name"], "is studying", student["track"])""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_python_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="python",
        defaults={
            "name": "Python",
            "icon": "\U0001F40D",
            "description": "A readable, general-purpose language popular for backends, data, and scripting.",
            "editor_language": "python",
            "order": 4,
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


def unseed_python_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="python").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0005_seed_js_subject"),
    ]

    operations = [
        migrations.RunPython(seed_python_subject, unseed_python_subject),
    ]
