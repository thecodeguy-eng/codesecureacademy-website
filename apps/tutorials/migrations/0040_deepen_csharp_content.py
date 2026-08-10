from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A statically-typed language from Microsoft, widely used with .NET — and where it fits alongside Java and C++.",
        "body": """
<p>C# (pronounced "C sharp") is a statically-typed, class-based language
built for the .NET platform — used for everything from web backends to
desktop apps to Unity games, the same broad reach Java has, built by a
different company with its own ecosystem.</p>

<h2>Example: a minimal C# program</h2>
<pre><code>using System;

class Program {
    static void Main() {
        Console.WriteLine("Hello, world!");
    }
}</code></pre>
<pre><code>Hello, world!</code></pre>
<p>Notice the structural similarity to Java: a class wrapping a
<code>Main</code> method, <code>Console.WriteLine</code> playing the same
role as Java's <code>System.out.println</code>. If you've already read
the Java tutorial, C#'s syntax should feel immediately recognizable —
both languages share deep roots in the same C-family tradition.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "Declaring typed variables — and the var keyword that lets the compiler infer the type for you.",
        "body": """
<p>C# variables need an explicit type: <code>int age = 21;</code>.</p>

<h2>Example: explicit type vs. var</h2>
<pre><code>using System;

class Program {
    static void Main() {
        string name = "Ada";
        var age = 21;
        Console.WriteLine($"{name} is {age} years old.");
    }
}</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p><code>var</code> lets the compiler infer the type from the assigned
value — <code>age</code> is still genuinely an <code>int</code> here,
fixed at compile time, just written without spelling the type out
explicitly. This is different from a dynamically-typed language: it's
purely a shorthand for the compiler to figure out what you clearly meant,
not permission for the variable to hold a different type later.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — the same C-family set as Java and C++.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison
(<code>== != &gt; &lt;</code>), and logical
(<code>&amp;&amp; || !</code>) operators work as in most C-family
languages.</p>

<h2>Example: a boolean expression, interpolated into output</h2>
<pre><code>using System;

class Program {
    static void Main() {
        int score = 85;
        bool passed = score >= 50 && score <= 100;
        Console.WriteLine($"Passed: {passed}");
    }
}</code></pre>
<pre><code>Passed: True</code></pre>
<p>Notice the capital <code>True</code> in the output — unlike C++ or
Java, C# actually prints its boolean values as the words
<code>True</code>/<code>False</code> directly, no ternary trick needed.
The <code>$"..."</code> syntax is a C# string interpolation, letting
<code>{passed}</code> be evaluated and inserted directly — the same
underlying idea as Python's f-strings or JavaScript's template literals,
just C#'s particular spelling of it.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, else if, and else — identical structure to Java and C++.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work the
same as in Java or C++.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>using System;

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
}</code></pre>
<pre><code>Good afternoon</code></pre>
<p>By now, if you've seen this same example in the Java or C++ sections
of this tutorial, the pattern should feel entirely familiar — that
repetition is deliberate: seeing the identical logic expressed in three
closely related languages is one of the fastest ways to internalize which
parts are "genuinely how branching works" versus "just this language's
particular syntax."</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for and while — the same three-part for-loop structure once again.",
        "body": """
<p>C#'s <code>for</code> loop uses the same three-part structure as Java
and C++: initializer, condition, update.</p>

<h2>Example: summing with a for loop</h2>
<pre><code>using System;

class Program {
    static void Main() {
        int total = 0;
        for (int i = 1; i <= 5; i++) {
            total += i;
        }
        Console.WriteLine($"Total: {total}");
    }
}</code></pre>
<pre><code>Total: 15</code></pre>
<p>C# also has a <code>foreach</code> loop for stepping through a
collection without managing an index — you'll meet it properly in the
Arrays lesson next, and it plays the exact same role as Java's enhanced
for-loop or PHP's <code>foreach</code>.</p>
""",
    },
    {
        "slug": "methods",
        "summary": "Reusable blocks of code, declared with a return type — C#'s term for the same idea Java calls methods too.",
        "body": """
<p>A method declares its return type, name, and parameters up front:
<code>static int Square(int n) { ... }</code>.</p>

<h2>Example: a static method</h2>
<pre><code>using System;

class Program {
    static string Greet(string name) {
        return $"Hello, {name}!";
    }

    static void Main() {
        Console.WriteLine(Greet("Chidi"));
    }
}</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>Notice C# method names conventionally start with a capital letter
(<code>Greet</code>, <code>Main</code>) — this is a real, widely-followed
naming convention in C# (called PascalCase), distinct from Java's
convention of starting method names lowercase (<code>greet</code>). Same
underlying concept, different community convention — worth knowing so
your code reads as idiomatic C#, not just "Java syntax translated."</p>
""",
    },
    {
        "slug": "arrays",
        "summary": "Fixed-size, single-type collections — and the foreach loop that steps through one cleanly.",
        "body": """
<p>An array holds a fixed number of same-typed values:
<code>int[] numbers = {1, 2, 3, 4, 5};</code>.</p>

<h2>Example: foreach over an array</h2>
<pre><code>using System;

class Program {
    static void Main() {
        int[] numbers = {1, 2, 3, 4, 5};
        int total = 0;
        foreach (int n in numbers) {
            total += n;
        }
        Console.WriteLine($"Total: {total}");
    }
}</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>foreach (int n in numbers)</code> steps through each value in
turn without needing a manual index — prefer it over a plain
<code>for</code> loop whenever you don't specifically need the index
itself. Get the count with <code>numbers.Length</code> (a property, no
parentheses) if you do need to know the size.</p>
""",
    },
    {
        "slug": "classes-and-objects",
        "summary": "Blueprints (classes) and the instances made from them (objects) — a constructor pattern almost identical to Java's.",
        "body": """
<p>A class describes the fields and methods its instances will have.
<code>new ClassName(...)</code> creates an object from that blueprint,
running the class's constructor to set up its initial data.</p>

<h2>Example: a Student class</h2>
<pre><code>using System;

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
}</code></pre>
<pre><code>Ada is studying Frontend</code></pre>
<p><code>public</code> before a field means it's accessible from outside
the class — without it, C# fields default to private, accessible only
from inside the class itself. This is a real, deliberate design choice
(called <strong>encapsulation</strong>) that comes up across almost every
object-oriented language, controlling exactly what outside code is
allowed to see and touch directly versus what stays as an internal
implementation detail.</p>
""",
    },
]


def deepen_csharp_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="csharp")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0039_deepen_cpp_content"),
    ]

    operations = [
        migrations.RunPython(deepen_csharp_content, noop),
    ]
