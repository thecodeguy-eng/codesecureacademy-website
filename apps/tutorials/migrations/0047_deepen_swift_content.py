from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "Apple's language for building iOS, iPadOS, and macOS apps — the modern replacement for Objective-C.",
        "body": """
<p>Swift is Apple's language for building apps across iOS, iPadOS, macOS,
and beyond — the modern replacement for Objective-C, Apple's older
language.</p>

<h2>Example: the simplest Swift program</h2>
<pre><code>print("Hello, world!")</code></pre>
<pre><code>Hello, world!</code></pre>
<p>Notice there's no wrapping function, no class, not even a semicolon —
Swift is designed to let a simple program stay genuinely simple. It's
statically typed and designed to catch common bugs (like using a value
that was never actually set) at compile time, similar in spirit to
Kotlin's approach to the same problem on the Android side.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "let vs var — Swift's own version of the const/val pattern this tutorial keeps coming back to.",
        "body": """
<p><code>let</code> declares a constant; <code>var</code> declares a
variable you can reassign.</p>

<h2>Example: preferring let by default</h2>
<pre><code>let name = "Ada"
var age = 21
print("\\(name) is \\(age) years old.")</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>By now this should feel familiar: <code>let</code> here plays the
exact same role as JavaScript's <code>const</code>, Kotlin's
<code>val</code>, and Dart's <code>final</code> — every one of these
modern languages independently converged on "prefer an unreassignable
value by default" as good practice. Swift infers the type from the
assigned value, or you can write it explicitly:
<code>let age: Int = 21</code>. Note Swift's string interpolation uses
backslash-parenthesis <code>\\( )</code>, not the dollar-brace
<code>${ }</code> or dollar-only <code>$name</code> styles other
languages in this tutorial use — a small but real syntax difference worth
remembering.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if/else, and Swift's switch statement for multi-way decisions.",
        "body": """
<p><code>if</code>/<code>else if</code>/<code>else</code> work as usual
— no parentheses needed around the condition, unlike most other
C-family languages in this tutorial.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>let hour = 14
let greeting: String

if hour < 12 {
    greeting = "Good morning"
} else if hour < 18 {
    greeting = "Good afternoon"
} else {
    greeting = "Good evening"
}

print(greeting)</code></pre>
<pre><code>Good afternoon</code></pre>
<p>Swift's <code>switch</code> is also commonly used for multi-way
branches, and unlike some languages, it doesn't silently fall through to
the next case by default — each case is self-contained, which avoids a
classic C/Java bug where a forgotten <code>break</code> lets execution
accidentally continue into the next case.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "for-in and while, and Swift's range syntax — including the subtle difference between ... and ..<.",
        "body": """
<p>Swift's <code>for-in</code> loop steps through a range or collection
directly.</p>

<h2>Example: two ranges, one small but important difference</h2>
<pre><code>var total = 0
for i in 1...5 {
    total += i
}
print("Total: \\(total)")</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>1...5</code> (three dots) includes both endpoints, 1 through 5.
<code>1..&lt;5</code> (two dots and a less-than) excludes the last one,
covering 1 through 4 only — a genuinely easy pair to mix up, and worth
double-checking whenever an off-by-one result shows up unexpectedly in
your own code.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Reusable blocks of code with func — and the argument labels that make Swift calls read almost like a sentence.",
        "body": """
<p>Declare a function with
<code>func name(parameter: Type) -&gt; ReturnType { ... }</code>.</p>

<h2>Example: a function call that reads naturally</h2>
<pre><code>func greet(name: String) -> String {
    return "Hello, \\(name)!"
}

print(greet(name: "Chidi"))</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>Notice the call site: <code>greet(name: "Chidi")</code>, not just
<code>greet("Chidi")</code>. Swift's function calls typically include
argument labels, which makes call sites read almost like a sentence —
genuinely useful once a function takes several parameters and a bare list
of values would otherwise be ambiguous about which value means what.</p>
""",
    },
    {
        "slug": "classes-and-structs",
        "summary": "Two ways to bundle data and behaviour — and the reference-vs-value difference that actually decides which one to reach for.",
        "body": """
<p>Swift has both <code>class</code> and <code>struct</code> for
bundling data and behaviour together.</p>

<h2>Example: a struct</h2>
<pre><code>struct Student {
    let name: String
    let track: String
}

let ada = Student(name: "Ada", track: "Frontend")
print("\\(ada.name) is studying \\(ada.track)")</code></pre>
<pre><code>Ada is studying Frontend</code></pre>
<p>The key difference between the two: a <code>class</code> is a
<strong>reference type</strong> — if you copy a class instance into
another variable, both variables point at the exact same underlying
object, so changing one changes what the other sees too. A
<code>struct</code> is a <strong>value type</strong> — copies are
completely independent, exactly like copying a plain number or string.
Apple recommends structs by default, reaching for classes only when you
specifically need shared, mutable state across multiple parts of your
code — the opposite default from Java or C#, where classes are the only
option for this kind of thing at all.</p>
""",
    },
]


def deepen_swift_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="swift")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0046_deepen_kotlin_content"),
    ]

    operations = [
        migrations.RunPython(deepen_swift_content, noop),
    ]
