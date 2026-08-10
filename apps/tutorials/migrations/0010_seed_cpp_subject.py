from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to C++",
        "slug": "introduction",
        "order": 1,
        "summary": "A fast, compiled language that gives you close control over memory.",
        "body": """
<p>C++ compiles down to machine code and gives you fine control over memory and performance
&mdash; it's used for games, operating systems, and other performance-critical software.
Every program needs a <code>main()</code> function, where execution starts.
<code>std::cout &lt;&lt;</code> prints output.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
    return 0;
}""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Variables & Data Types",
        "slug": "variables-and-data-types",
        "order": 2,
        "summary": "Declaring typed variables: int, double, bool, string.",
        "body": """
<p>Like Java, C++ variables need an explicit type: <code>int age = 21;</code>. Common types:
<code>int</code>, <code>double</code>, <code>bool</code>, and <code>string</code> (from the
<code>&lt;string&gt;</code> header).</p>
""",
        "example_code": """#include <iostream>
#include <string>
using namespace std;

int main() {
    string name = "Ada";
    int age = 21;
    cout << name << " is " << age << " years old." << endl;
    return 0;
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
        "example_code": """#include <iostream>
using namespace std;

int main() {
    int score = 85;
    bool passed = score >= 50 && score <= 100;
    cout << "Passed: " << (passed ? "true" : "false") << endl;
    return 0;
}""",
        "expected_output": "Passed: true",
    },
    {
        "title": "Conditionals",
        "slug": "conditionals",
        "order": 4,
        "summary": "Branching with if, else if, and else.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> behave the same as in Java
or JavaScript &mdash; conditions in parentheses, blocks in curly braces.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int main() {
    int hour = 14;
    string greeting;

    if (hour < 12) {
        greeting = "Good morning";
    } else if (hour < 18) {
        greeting = "Good afternoon";
    } else {
        greeting = "Good evening";
    }

    cout << greeting << endl;
    return 0;
}""",
        "expected_output": "Good afternoon",
    },
    {
        "title": "Loops",
        "slug": "loops",
        "order": 5,
        "summary": "Repeating code with for and while.",
        "body": """
<p>C++'s <code>for</code> loop follows the same three-part structure as Java and
JavaScript: initializer, condition, update.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int main() {
    int total = 0;
    for (int i = 1; i <= 5; i++) {
        total += i;
    }
    cout << "Total: " << total << endl;
    return 0;
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 6,
        "summary": "Reusable blocks of code with a declared return type.",
        "body": """
<p>A function declares its return type, name, and parameter types up front:
<code>int add(int a, int b) { ... }</code>. Use <code>void</code> as the return type for a
function that doesn't return a value.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int square(int n) {
    return n * n;
}

int main() {
    cout << "Square of 6 is " << square(6) << endl;
    return 0;
}""",
        "expected_output": "Square of 6 is 36",
    },
    {
        "title": "Arrays",
        "slug": "arrays",
        "order": 7,
        "summary": "Fixed-size, single-type collections.",
        "body": """
<p>An array holds a fixed number of same-typed values:
<code>int numbers[5] = {1, 2, 3, 4, 5};</code>. Access items by zero-based index
(<code>numbers[0]</code>). Unlike Java, C++ arrays don't know their own length &mdash; you
have to track it yourself.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    int total = 0;
    for (int i = 0; i < 5; i++) {
        total += numbers[i];
    }
    cout << "Total: " << total << endl;
    return 0;
}""",
        "expected_output": "Total: 15",
    },
    {
        "title": "Pointers (Basics)",
        "slug": "pointers",
        "order": 8,
        "summary": "Variables that store a memory address instead of a value.",
        "body": """
<p>A pointer stores the memory <em>address</em> of another variable, rather than a value
directly. Declare one with <code>*</code> (<code>int* p;</code>), and get a variable's
address with <code>&</code>. Pointers are one of the things that give C++ its low-level
control &mdash; and one of the things that make it easy to make mistakes, so most modern C++
code prefers references and smart pointers where possible. This is just the basic idea.</p>
""",
        "example_code": """#include <iostream>
using namespace std;

int main() {
    int age = 21;
    int* agePointer = &age;

    cout << "Value: " << *agePointer << endl;
    cout << "Address stored in pointer: " << agePointer << endl;
    return 0;
}""",
        "expected_output": "Value: 21\nAddress stored in pointer: 0x7ffeeb1c2a9c   (a real address will differ each run)",
    },
]


def seed_cpp_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="cpp",
        defaults={
            "name": "C++",
            "icon": "⚙️",
            "description": "A fast, compiled language with close control over memory — used for games, systems, and performance-critical software.",
            "editor_language": "cpp",
            "order": 8,
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


def unseed_cpp_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="cpp").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0009_seed_java_subject"),
    ]

    operations = [
        migrations.RunPython(seed_cpp_subject, unseed_cpp_subject),
    ]
