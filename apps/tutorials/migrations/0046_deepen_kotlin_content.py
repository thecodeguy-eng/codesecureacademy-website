from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "Google's preferred language for building Android apps — and why it's genuinely safer than Java in one specific, common way.",
        "body": """
<p>Kotlin is a statically-typed language that runs on the same JVM Java
does, and is Google's preferred language for Android development.</p>

<h2>Example: a minimal Kotlin program</h2>
<pre><code>fun main() {
    println("Hello, world!")
}</code></pre>
<pre><code>Hello, world!</code></pre>
<p>Kotlin can call any existing Java code directly, but with more concise
syntax — <code>fun main()</code> needs no wrapping class the way Java's
<code>public class Main { public static void main(...) }</code> does.
Kotlin also catches a lot of "null" errors at compile time instead of at
runtime: a variable's type has to explicitly allow <code>null</code>
(written <code>String?</code> instead of just <code>String</code>) before
it's even permitted to hold one, which prevents an entire, very common
category of Java crash from happening in the first place.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "val vs var — and why val should be your default, mirroring the same preference from JavaScript's const.",
        "body": """
<p><code>val</code> declares a value that can't be reassigned; <code>var</code>
declares one that can.</p>

<h2>Example: preferring val, using var only when needed</h2>
<pre><code>fun main() {
    val name = "Ada"
    var age = 21
    println("$name is $age years old.")
}</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>Prefer <code>val</code> by default — the exact same recommendation the
JavaScript tutorial gives for <code>const</code> over <code>let</code>,
for the same reason: it prevents an accidental reassignment from
compiling at all, catching a mistake immediately instead of it silently
happening somewhere unexpected. Kotlin usually infers the type from the
assigned value, though you can write it explicitly:
<code>val age: Int = 21</code>.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if/else — and how if can be used as an expression that directly produces a value.",
        "body": """
<p><code>if</code>/<code>else if</code>/<code>else</code> work as usual,
but in Kotlin <code>if</code> can also be used as an
<strong>expression</strong> that directly produces a value.</p>

<h2>Example: if as an expression</h2>
<pre><code>fun main() {
    val hour = 14
    val greeting = if (hour < 12) "Good morning" else if (hour < 18) "Good afternoon" else "Good evening"
    println(greeting)
}</code></pre>
<pre><code>Good afternoon</code></pre>
<p>This single line replaces what a separate ternary operator does in
languages like Java or JavaScript — Kotlin doesn't have a
<code>? :</code> ternary at all, since <code>if</code>/<code>else</code>
used as an expression already covers the same need, arguably more
readably once you're used to it.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "for and while, and Kotlin's inclusive range syntax.",
        "body": """
<p>Kotlin's <code>for</code> loop steps through a range or collection
directly: <code>for (i in 1..5)</code> includes both endpoints.</p>

<h2>Example: summing an inclusive range</h2>
<pre><code>fun main() {
    var total = 0
    for (i in 1..5) {
        total += i
    }
    println("Total: $total")
}</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>1..5</code> is a range literal that includes both 1 and 5 —
compare Swift's very similar <code>1...5</code> in the Swift subject of
this tutorial, or a plain <code>for (int i = 1; i &lt;= 5; i++)</code> in
Java or C#, which achieves the identical result with more ceremony.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Reusable blocks of code with fun — and the short single-expression syntax.",
        "body": """
<p>Declare a function with <code>fun name(params): ReturnType { ... }</code>.
For a one-line function, you can skip the braces and use <code>=</code>
instead.</p>

<h2>Example: a single-expression function</h2>
<pre><code>fun greet(name: String): String = "Hello, $name!"

fun main() {
    println(greet("Chidi"))
}</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>This is the same underlying idea as Dart's arrow functions or a
Python lambda — a function whose entire body is one expression doesn't
need the full <code>{ return ... }</code> ceremony. Kotlin can even infer
the return type here from the expression itself, though writing it
explicitly (as above) keeps the function's contract clear at a glance.</p>
""",
    },
    {
        "slug": "classes-and-objects",
        "summary": "Kotlin's concise class syntax, including data classes — and the boilerplate they eliminate.",
        "body": """
<p>A class's constructor parameters can be declared right in the class
header, dramatically shortening what would be several lines in Java.</p>

<h2>Example: a data class</h2>
<pre><code>data class Student(val name: String, val track: String)

fun main() {
    val ada = Student("Ada", "Frontend")
    println("${ada.name} is studying ${ada.track}")
}</code></pre>
<pre><code>Ada is studying Frontend</code></pre>
<p>Compare this one line to Java's Student class from the Java tutorial —
Kotlin's <code>data class</code> automatically generates useful
boilerplate a Java class needs written by hand: a readable
<code>toString()</code>, equality checks comparing actual field values
instead of just object identity, and more. This is exactly what makes it
the right choice for classes that are mainly just holding data — which is
precisely what most Android UI models look like in practice.</p>
""",
    },
]


def deepen_kotlin_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="kotlin")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0045_deepen_linux_content"),
    ]

    operations = [
        migrations.RunPython(deepen_kotlin_content, noop),
    ]
