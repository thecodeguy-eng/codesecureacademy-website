from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Swift",
        "slug": "introduction",
        "order": 1,
        "summary": "Apple's language for building iOS, iPadOS, and macOS apps.",
        "body": """
<p>Swift is Apple's language for building apps across iOS, iPadOS, macOS, and beyond
&mdash; the modern replacement for Objective-C. It's statically typed and designed to catch
common bugs (like using a value that was never set) at compile time.
<code>print()</code> outputs a line, and unlike C-family languages, Swift doesn't require a
separate <code>main()</code> function or semicolons at the end of each line.</p>
""",
        "example_code": 'print("Hello, world!")',
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "let vs var, and Swift's core types.",
        "body": """
<p><code>let</code> declares a constant (prefer this by default); <code>var</code>
declares a variable you can reassign. Swift infers the type from the assigned value, or you
can write it explicitly: <code>let age: Int = 21</code>.</p>
""",
        "example_code": """let name = "Ada"
var age = 21
print("\\(name) is \\(age) years old.")""",
        "expected_output": "Ada is 21 years old.",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 3,
        "summary": "Branching with if/else, and Swift's switch statement.",
        "body": """
<p><code>if</code>/<code>else if</code>/<code>else</code> work as usual (no parentheses
needed around the condition). Swift's <code>switch</code> is also commonly used for
multi-way branches, and unlike some other languages, it doesn't fall through to the next
case by default.</p>
""",
        "example_code": """let hour = 14
let greeting: String

if hour < 12 {
    greeting = "Good morning"
} else if hour < 18 {
    greeting = "Good afternoon"
} else {
    greeting = "Good evening"
}

print(greeting)""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 4,
        "summary": "for-in and while, and Swift's range syntax.",
        "body": """
<p>Swift's <code>for-in</code> loop steps through a range or collection directly:
<code>for i in 1...5</code> includes both endpoints (three dots excludes the last one).
<code>while</code> works as in most other languages.</p>
""",
        "example_code": """var total = 0
for i in 1...5 {
    total += i
}
print("Total: \\(total)")""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 5,
        "summary": "Reusable blocks of code with func.",
        "body": """
<p>Declare a function with <code>func name(parameter: Type) -&gt; ReturnType { ... }</code>.
Swift's function calls typically include argument labels, which makes call sites read
almost like a sentence.</p>
""",
        "example_code": """func greet(name: String) -> String {
    return "Hello, \\(name)!"
}

print(greet(name: "Chidi"))""",
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Classes & Structs",
        "slug": "classes-and-structs",
        "order": 6,
        "summary": "Two ways to bundle data and behaviour, with an important difference.",
        "body": """
<p>Swift has both <code>class</code> and <code>struct</code> for bundling data and
behaviour together. The key difference: a <code>class</code> is a reference type (copies
share the same underlying data), while a <code>struct</code> is a value type (copies are
independent). Apple recommends structs by default, reaching for classes only when you
specifically need shared, mutable state.</p>
""",
        "example_code": """struct Student {
    let name: String
    let track: String
}

let ada = Student(name: "Ada", track: "Frontend")
print("\\(ada.name) is studying \\(ada.track)")""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_swift_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    app_dev = Category.objects.get(slug="app-development")

    subject, _ = Subject.objects.update_or_create(
        slug="swift",
        defaults={
            "category": app_dev,
            "name": "Swift",
            "icon": "\U0001F426",
            "description": "Apple's language for building iOS, iPadOS, and macOS apps.",
            "editor_language": "swift",
            "order": 13,
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


def unseed_swift_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="swift").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0026_seed_kotlin_subject"),
    ]

    operations = [
        migrations.RunPython(seed_swift_subject, unseed_swift_subject),
    ]
