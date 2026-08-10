from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Kotlin",
        "slug": "introduction",
        "order": 1,
        "summary": "Google's preferred language for building Android apps.",
        "body": """
<p>Kotlin is a statically-typed language that runs on the same JVM Java does, and is
Google's preferred language for Android development &mdash; it can call any existing Java
code, but with more concise, safer syntax (in particular, catching a lot of "null" errors at
compile time instead of at runtime). <code>fun main()</code> is the entry point, and
<code>println()</code> prints a line.</p>
""",
        "example_code": """fun main() {
    println("Hello, world!")
}""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "val vs var, and Kotlin's core types.",
        "body": """
<p><code>val</code> declares a value that can't be reassigned (prefer this by default);
<code>var</code> declares one that can. Kotlin usually infers the type from the assigned
value, though you can write it explicitly: <code>val age: Int = 21</code>.</p>
""",
        "example_code": """fun main() {
    val name = "Ada"
    var age = 21
    println("$name is $age years old.")
}""",
        "expected_output": "Ada is 21 years old.",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 3,
        "summary": "Branching with if/else — and if as an expression.",
        "body": """
<p><code>if</code>/<code>else if</code>/<code>else</code> work as usual, but in Kotlin
<code>if</code> can also be used as an <strong>expression</strong> that directly produces a
value, often replacing a separate ternary operator.</p>
""",
        "example_code": """fun main() {
    val hour = 14
    val greeting = if (hour < 12) "Good morning" else if (hour < 18) "Good afternoon" else "Good evening"
    println(greeting)
}""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 4,
        "summary": "for and while, and Kotlin's range syntax.",
        "body": """
<p>Kotlin's <code>for</code> loop steps through a range or collection directly:
<code>for (i in 1..5)</code> includes both endpoints. <code>while</code> works as in most
other languages.</p>
""",
        "example_code": """fun main() {
    var total = 0
    for (i in 1..5) {
        total += i
    }
    println("Total: $total")
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 5,
        "summary": "Reusable blocks of code with fun.",
        "body": """
<p>Declare a function with <code>fun name(params): ReturnType { ... }</code>. For a
one-line function, you can skip the braces and use <code>=</code> instead.</p>
""",
        "example_code": """fun greet(name: String): String = "Hello, $name!"

fun main() {
    println(greet("Chidi"))
}""",
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Classes & Objects",
        "slug": "classes-and-objects",
        "order": 6,
        "summary": "Kotlin's concise class syntax, including data classes.",
        "body": """
<p>A class's constructor parameters can be declared right in the class header. A
<code>data class</code> automatically generates useful boilerplate &mdash; a readable
<code>toString()</code>, equality checks, and more &mdash; for classes that are mainly just
holding data, which is exactly what most Android UI models look like.</p>
""",
        "example_code": """data class Student(val name: String, val track: String)

fun main() {
    val ada = Student("Ada", "Frontend")
    println("${ada.name} is studying ${ada.track}")
}""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_kotlin_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    app_dev = Category.objects.get(slug="app-development")

    subject, _ = Subject.objects.update_or_create(
        slug="kotlin",
        defaults={
            "category": app_dev,
            "name": "Kotlin",
            "icon": "\U0001F7E3",
            "description": "Google's preferred language for building Android apps.",
            "editor_language": "kotlin",
            "order": 12,
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


def unseed_kotlin_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="kotlin").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0025_fix_double_escaped_ampersands"),
    ]

    operations = [
        migrations.RunPython(seed_kotlin_subject, unseed_kotlin_subject),
    ]
