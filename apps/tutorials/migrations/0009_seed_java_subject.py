from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Java",
        "slug": "introduction",
        "order": 1,
        "summary": "A statically-typed, compiled language built around classes.",
        "body": """
<p>Java is a statically-typed language &mdash; every variable's type is fixed and checked
before the program runs. Every Java program lives inside at least one <strong>class</strong>,
and execution starts from a special <code>main</code> method.
<code>System.out.println()</code> prints a line of output.</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "Declaring typed variables: int, double, boolean, String.",
        "body": """
<p>Unlike Python or JavaScript, Java variables need an explicit type when declared:
<code>int age = 21;</code>. Common types include <code>int</code> (whole numbers),
<code>double</code> (decimals), <code>boolean</code> (true/false), and
<code>String</code> (text, capitalised &mdash; it's a class, not a primitive type).</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        String name = "Ada";
        int age = 21;
        System.out.println(name + " is " + age + " years old.");
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
logical (<code>&& || !</code>) operators work much like other C-family languages.
Note <code>==</code> compares object references for non-primitive types like
<code>String</code>, so strings are usually compared with <code>.equals()</code> instead.</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        int score = 85;
        boolean passed = score >= 50 && score <= 100;
        System.out.println("Passed: " + passed);
    }
}""",
        "expected_output": "Passed: true",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 4,
        "summary": "Branching with if, else if, and else.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work as in most C-family
languages, with each condition wrapped in parentheses and each block in curly braces.</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        int hour = 14;
        String greeting;

        if (hour < 12) {
            greeting = "Good morning";
        } else if (hour < 18) {
            greeting = "Good afternoon";
        } else {
            greeting = "Good evening";
        }

        System.out.println(greeting);
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
<p>Java's <code>for</code> loop has three parts: a starting statement, a continue condition,
and an update step, all separated by semicolons. <code>while</code> repeats as long as its
condition holds.</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 5; i++) {
            total += i;
        }
        System.out.println("Total: " + total);
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
<p>A method's signature declares what type it returns (or <code>void</code> for nothing),
its name, and its parameters &mdash; each with its own type. Call it by name, passing
matching arguments.</p>
""",
        "example_code": """public class Main {
    static String greet(String name) {
        return "Hello, " + name + "!";
    }

    public static void main(String[] args) {
        System.out.println(greet("Chidi"));
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
<p>An array holds a fixed number of values of one type:
<code>int[] numbers = {1, 2, 3, 4, 5};</code>. Access items by zero-based index
(<code>numbers[0]</code>), and get the length with <code>numbers.length</code> (a field,
not a method).</p>
""",
        "example_code": """public class Main {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        int total = 0;
        for (int n : numbers) {
            total += n;
        }
        System.out.println("Total: " + total);
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
<p>A class is a blueprint describing what data (fields) and behaviour (methods) its
instances will have. <code>new ClassName(...)</code> creates an <strong>object</strong> from
that blueprint &mdash; each object gets its own copy of the fields.</p>
""",
        "example_code": """class Student {
    String name;
    String track;

    Student(String name, String track) {
        this.name = name;
        this.track = track;
    }
}

public class Main {
    public static void main(String[] args) {
        Student ada = new Student("Ada", "Frontend");
        System.out.println(ada.name + " is studying " + ada.track);
    }
}""",
        "expected_output": "Ada is studying Frontend",
    },
]


def seed_java_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="java",
        defaults={
            "name": "Java",
            "icon": "☕",
            "description": "A statically-typed, class-based language widely used in enterprise software.",
            "editor_language": "java",
            "order": 7,
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


def unseed_java_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="java").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0008_seed_sql_subject"),
    ]

    operations = [
        migrations.RunPython(seed_java_subject, unseed_java_subject),
    ]
