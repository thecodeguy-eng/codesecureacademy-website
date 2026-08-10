from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to C#",
        "slug": "introduction",
        "order": 1,
        "summary": "A statically-typed language from Microsoft, widely used with .NET.",
        "body": """
<p>C# (pronounced "C sharp") is a statically-typed, class-based language built for the .NET
platform &mdash; used for everything from web backends to desktop apps to Unity games.
Every program has a <code>Main</code> method where execution starts, and
<code>Console.WriteLine()</code> prints a line of output.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, world!");
    }
}""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "Declaring typed variables: int, double, bool, string.",
        "body": """
<p>C# variables need an explicit type: <code>int age = 21;</code>. Common types:
<code>int</code>, <code>double</code>, <code>bool</code>, and <code>string</code>
(capitalised, like Java). You can also use <code>var</code> and let the compiler infer the
type from the assigned value.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        string name = "Ada";
        int age = 21;
        Console.WriteLine($"{name} is {age} years old.");
    }
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
logical (<code>&& || !</code>) operators work as in most C-family languages.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        int score = 85;
        bool passed = score >= 50 && score <= 100;
        Console.WriteLine($"Passed: {passed}");
    }
}""",
        "expected_output": "Passed: True",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 4,
        "summary": "Branching with if, else if, and else.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work the same as in Java or
C++ &mdash; conditions in parentheses, blocks in curly braces.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        int hour = 14;
        string greeting;

        if (hour < 12) {
            greeting = "Good morning";
        } else if (hour < 18) {
            greeting = "Good afternoon";
        } else {
            greeting = "Good evening";
        }

        Console.WriteLine(greeting);
    }
}""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 5,
        "summary": "Repeating code with for and while.",
        "body": """
<p>C#'s <code>for</code> loop uses the same three-part structure as Java and C++:
initializer, condition, update.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        int total = 0;
        for (int i = 1; i <= 5; i++) {
            total += i;
        }
        Console.WriteLine($"Total: {total}");
    }
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Methods",
        "slug": "methods",
        "order": 6,
        "summary": "Reusable blocks of code, declared with a return type.",
        "body": """
<p>A method declares its return type, name, and parameters up front:
<code>static int Square(int n) { ... }</code>. Use <code>void</code> for a method that
doesn't return a value.</p>
""",
        "example_code": """using System;

class Program {
    static string Greet(string name) {
        return $"Hello, {name}!";
    }

    static void Main() {
        Console.WriteLine(Greet("Chidi"));
    }
}""",
        "expected_output": "Hello, Chidi!",
    },
    {
        "title": "Arrays",
        "slug": "arrays",
        "order": 7,
        "summary": "Fixed-size, single-type collections.",
        "body": """
<p>An array holds a fixed number of same-typed values:
<code>int[] numbers = {1, 2, 3, 4, 5};</code>. Access items by zero-based index, and get the
count with <code>numbers.Length</code>.</p>
""",
        "example_code": """using System;

class Program {
    static void Main() {
        int[] numbers = {1, 2, 3, 4, 5};
        int total = 0;
        foreach (int n in numbers) {
            total += n;
        }
        Console.WriteLine($"Total: {total}");
    }
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Classes & Objects",
        "slug": "classes-and-objects",
        "order": 8,
        "summary": "Blueprints (classes) and the instances made from them (objects).",
        "body": """
<p>A class describes the fields and methods its instances will have.
<code>new ClassName(...)</code> creates an object from that blueprint, running the class's
constructor to set up its initial data.</p>
""",
        "example_code": """using System;

class Student {
    public string Name;
    public string Track;

    public Student(string name, string track) {
        Name = name;
        Track = track;
    }
}

class Program {
    static void Main() {
        Student ada = new Student("Ada", "Frontend");
        Console.WriteLine($"{ada.Name} is studying {ada.Track}");
    }
}""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_csharp_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="csharp",
        defaults={
            "name": "C#",
            "icon": "\U0001F538",
            "description": "A statically-typed, class-based language from Microsoft, widely used with .NET.",
            "editor_language": "csharp",
            "order": 9,
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


def unseed_csharp_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="csharp").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0010_seed_cpp_subject"),
    ]

    operations = [
        migrations.RunPython(seed_csharp_subject, unseed_csharp_subject),
    ]
