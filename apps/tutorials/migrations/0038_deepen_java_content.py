from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A statically-typed, compiled language built around classes — and why every Java program needs a class wrapper, even for one line.",
        "body": """
<p>Java is a statically-typed language — every variable's type is fixed
and checked before the program even runs, catching a whole category of
mistakes before your code ever executes, not while it's running.</p>

<h2>Example: the minimum a Java program needs</h2>
<pre><code>public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}</code></pre>
<pre><code>Hello, world!</code></pre>
<p>Every Java program lives inside at least one <strong>class</strong>,
and execution starts from a special <code>main</code> method — unlike
Python or JavaScript, there's no way to run a bare line of code outside a
class at all. This ceremony exists because Java is fundamentally
class-based: even "hello world" has to live somewhere, and that somewhere
is always a class.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "Declaring typed variables — and the specific error you get if you get the type wrong, unlike in Python or JavaScript.",
        "body": """
<p>Unlike Python or JavaScript, Java variables need an explicit type when
declared: <code>int age = 21;</code>.</p>

<h2>Example: declaring several typed variables</h2>
<pre><code>public class Main {
    public static void main(String[] args) {
        String name = "Ada";
        int age = 21;
        System.out.println(name + " is " + age + " years old.");
    }
}</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>Common types: <code>int</code> (whole numbers), <code>double</code>
(decimals), <code>boolean</code> (true/false), and <code>String</code>
(text — capitalised, since it's technically a class, not a primitive
type like the others). Try assigning a number to <code>name</code>
instead of text, and Java refuses to even compile the program — this
compile-time type checking is exactly what "statically-typed" means in
practice, not just a definition to memorize.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — and why comparing text needs .equals(), not ==.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison
(<code>== != &gt; &lt;</code>), and logical (<code>&amp;&amp; || !</code>)
operators work much like other C-family languages.</p>

<h2>Example: a boolean expression</h2>
<pre><code>public class Main {
    public static void main(String[] args) {
        int score = 85;
        boolean passed = score >= 50 && score <= 100;
        System.out.println("Passed: " + passed);
    }
}</code></pre>
<pre><code>Passed: true</code></pre>
<p>One Java-specific trap worth knowing early: <code>==</code> compares
object references for non-primitive types like <code>String</code>, not
their actual text content — two separately-created strings with identical
text can compare as <em>not equal</em> with <code>==</code>. Strings are
almost always compared with <code>.equals()</code> instead:
<code>name.equals("Ada")</code>, not <code>name == "Ada"</code>.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, else if, and else — familiar C-family structure.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work as
in most C-family languages, condition in parentheses, block in curly
braces.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>public class Main {
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
}</code></pre>
<pre><code>Good afternoon</code></pre>
<p>Notice <code>greeting</code> is declared without a value first, then
assigned inside whichever branch actually runs — Java requires it be
assigned exactly once along every possible path before it's used, or the
compiler refuses to build the program, another example of Java catching
a potential mistake before the code ever runs.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for and while — the same three-part for-loop shape as most C-family languages.",
        "body": """
<p>Java's <code>for</code> loop has three parts: a starting statement, a
continue condition, and an update step, all separated by semicolons.</p>

<h2>Example: summing with a for loop</h2>
<pre><code>public class Main {
    public static void main(String[] args) {
        int total = 0;
        for (int i = 1; i <= 5; i++) {
            total += i;
        }
        System.out.println("Total: " + total);
    }
}</code></pre>
<pre><code>Total: 15</code></pre>
<p>This exact three-part <code>for (start; condition; update)</code>
shape appears, essentially unchanged, in JavaScript, C, C++, and C# —
learning it once here transfers almost directly to every other
C-family language you might pick up later, which is a big part of why
starting with a language like Java or C++ makes the syntax of many other
languages feel immediately familiar.</p>
""",
    },
    {
        "slug": "methods",
        "summary": "Reusable blocks of code, declared with a return type — the term Java uses for what other languages call a function.",
        "body": """
<p>A method's signature declares what type it returns (or
<code>void</code> for nothing), its name, and its parameters — each with
its own declared type.</p>

<h2>Example: a static method and calling it</h2>
<pre><code>public class Main {
    static String greet(String name) {
        return "Hello, " + name + "!";
    }

    public static void main(String[] args) {
        System.out.println(greet("Chidi"));
    }
}</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>Java calls these <strong>methods</strong> rather than "functions"
specifically because they live inside a class — a bare, standalone
function outside any class doesn't exist in Java the way it does in
Python or JavaScript. The <code>static</code> keyword here means this
particular method belongs to the class itself, not to any specific object
instance of it — you'll meet the distinction properly in the
Classes &amp; Objects lesson.</p>
""",
    },
    {
        "slug": "arrays",
        "summary": "Fixed-size, single-type collections — and the enhanced for-loop that steps through one without an index.",
        "body": """
<p>An array holds a fixed number of values of one type:
<code>int[] numbers = {1, 2, 3, 4, 5};</code>.</p>

<h2>Example: an enhanced for-loop over an array</h2>
<pre><code>public class Main {
    public static void main(String[] args) {
        int[] numbers = {1, 2, 3, 4, 5};
        int total = 0;
        for (int n : numbers) {
            total += n;
        }
        System.out.println("Total: " + total);
    }
}</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>for (int n : numbers)</code> — read "for each int n in
numbers" — is Java's <strong>enhanced for-loop</strong>, and is generally
preferred over a manual index-based loop whenever you don't actually need
the index itself, just each value in turn. Access individual items by
zero-based index (<code>numbers[0]</code>), and get the length with
<code>numbers.length</code> — a field, not a method, so no parentheses.</p>
""",
    },
    {
        "slug": "classes-and-objects",
        "summary": "Blueprints (classes) and the instances made from them (objects) — where 'new' actually comes from.",
        "body": """
<p>A class is a blueprint describing what data (fields) and behaviour
(methods) its instances will have. <code>new ClassName(...)</code>
creates an <strong>object</strong> from that blueprint.</p>

<h2>Example: a Student class and creating an instance</h2>
<pre><code>class Student {
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
}</code></pre>
<pre><code>Ada is studying Frontend</code></pre>
<p>The block matching the class name (<code>Student(String name, String track) {...}</code>)
is the <strong>constructor</strong> — it runs automatically every time
<code>new Student(...)</code> is called, setting up that specific
object's initial data. <code>this.name = name</code> distinguishes the
object's own field (<code>this.name</code>) from the constructor's
parameter (<code>name</code>), which otherwise share the identical name —
a deliberate, very common naming convention, not a coincidence, and worth
recognizing when you see it in real code.</p>
""",
    },
]


def deepen_java_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="java")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0037_deepen_sql_content"),
    ]

    operations = [
        migrations.RunPython(deepen_java_content, noop),
    ]
