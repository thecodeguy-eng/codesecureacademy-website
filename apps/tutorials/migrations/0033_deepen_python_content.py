from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "Why Python reads almost like plain English, how print() works, and why it's such a common first language.",
        "body": """
<p>Python is a general-purpose programming language known for clean,
readable syntax — it uses indentation instead of curly braces to mark
blocks of code, which forces consistently formatted code across every
project and every developer who touches it.</p>

<h2>Example: the simplest possible program</h2>
<pre><code>print("Hello, world!")</code></pre>
<p><code>print()</code> outputs a value. Compare this single line to the
equivalent in a language like Java or C#, which needs a whole class and
method wrapper just to print one line — Python's minimal ceremony is a
big part of why it's such a common first language, and why it's also
popular for quick scripts and data work where you want to focus on the
actual problem, not boilerplate.</p>

<p>These examples are shown read-only here (no in-browser Python
execution), with the expected output shown below each one so you can
follow along without needing Python installed yet.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "Assigning values without declaring a type, and Python's core built-in types.",
        "body": """
<p>Python variables don't need a declared type — just assign a value with
<code>=</code> and Python figures out the type from what you assigned.</p>

<h2>Example: checking a variable's type</h2>
<pre><code>name = "Ada"
age = 21
gpa = 3.8

print(type(name), type(age), type(gpa))</code></pre>
<pre><code>&lt;class 'str'&gt; &lt;class 'int'&gt; &lt;class 'float'&gt;</code></pre>
<p>The core built-in types: <code>str</code> (text), <code>int</code>
(whole numbers), <code>float</code> (decimals), and <code>bool</code>
(<code>True</code>/<code>False</code>). Note Python distinguishes
<code>int</code> from <code>float</code> — unlike JavaScript, which uses
one number type for both — which matters the moment you divide two whole
numbers and get a decimal result back.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — including the two division operators Python offers.",
        "body": """
<p>Arithmetic operators (<code>+ - * /</code>) do math, and
<code>//</code> and <code>%</code> give integer division and remainder.</p>

<h2>Example: the two kinds of division</h2>
<pre><code>print(7 / 2)   # 3.5   — normal division, always returns a float
print(7 // 2)  # 3     — integer division, drops the remainder
print(7 % 2)   # 1     — the remainder itself

score = 85
passed = score >= 50 and score <= 100
print("Passed:", passed)</code></pre>
<p><code>and</code>, <code>or</code>, and <code>not</code> are Python's
logical operators — spelled out as words rather than symbols like
<code>&amp;&amp;</code>/<code>||</code> in many other languages, which is
part of what gives Python its readable feel.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, elif, and else — and why indentation isn't just style here, it's the syntax.",
        "body": """
<p><code>if</code> runs a block only when its condition is true.
<code>elif</code> ("else if") checks another condition if the first was
false, and <code>else</code> catches everything else.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>hour = 14

if hour < 12:
    greeting = "Good morning"
elif hour < 18:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

print(greeting)</code></pre>
<pre><code>Good afternoon</code></pre>
<p>Python uses indentation — not curly braces — to mark which lines
belong to which block. This isn't optional style here the way it is in
many languages: inconsistent indentation is an actual syntax error in
Python, not just something a linter complains about. That constraint is
deliberate — it makes it structurally impossible to write Python code
where the indentation lies about what the code actually does.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for and while, and what range() actually produces.",
        "body": """
<p>A <code>for</code> loop steps through a sequence — often the result of
<code>range(n)</code>, which produces the numbers 0 up to (not including)
<code>n</code>.</p>

<h2>Example: summing a range</h2>
<pre><code>total = 0
for i in range(1, 6):
    total += i

print("Total:", total)</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>range(1, 6)</code> produces 1, 2, 3, 4, 5 — the second number is
the stopping point, not included, which trips up nearly every beginner at
least once. A <code>while</code> loop, by contrast, repeats as long as
its condition stays true, and is the better tool whenever you don't know
the number of iterations in advance.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Defining reusable logic with def, and how f-strings make building output readable.",
        "body": """
<p>Define a function with <code>def name(parameters):</code>, followed by
an indented block, and <code>return</code> a value if it should produce
one.</p>

<h2>Example: a function using an f-string</h2>
<pre><code>def greet(name):
    return f"Hello, {name}!"

print(greet("Chidi"))</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>The <code>f</code> before the opening quote makes it an
<strong>f-string</strong> — anything inside curly braces gets evaluated
and inserted directly into the string. This is the standard, readable way
to build strings containing variables in modern Python, and is generally
preferred over older approaches like manually joining strings with
<code>+</code>.</p>
""",
    },
    {
        "slug": "lists",
        "summary": "Ordered, changeable collections — including the list comprehension shortcut for transforming one list into another.",
        "body": """
<p>A list holds an ordered collection of values: <code>fruits = ["apple", "banana"]</code>.
Access items by zero-based index (<code>fruits[0]</code>), and add with
<code>.append()</code>.</p>

<h2>Example: a list comprehension</h2>
<pre><code>numbers = [1, 2, 3, 4, 5]
doubled = [n * 2 for n in numbers]

print(doubled)</code></pre>
<pre><code>[2, 4, 6, 8, 10]</code></pre>
<p><code>[n * 2 for n in numbers]</code> is a <strong>list
comprehension</strong> — a compact way to build a new list by transforming
every item in an existing one. It's equivalent to writing a full
<code>for</code> loop that appends to an empty list one item at a time,
just shorter and, once the syntax is familiar, more readable at a glance.
It's a genuinely idiomatic Python pattern worth learning early, since
you'll see it constantly in real Python code.</p>
""",
    },
    {
        "slug": "dictionaries",
        "summary": "Key/value pairs for grouping related data, and the safe way to read a key that might not exist.",
        "body": """
<p>A dictionary groups values under named keys:
<code>student = {"name": "Ada", "track": "Frontend"}</code>.</p>

<h2>Example: two ways to read a value</h2>
<pre><code>student = {"name": "Ada", "track": "Frontend"}
print(student["name"], "is studying", student["track"])
print(student.get("age", "not provided"))</code></pre>
<pre><code>Ada is studying Frontend
not provided</code></pre>
<p><code>student["name"]</code> raises an error if the key doesn't
exist. <code>student.get("age", "not provided")</code> instead returns a
fallback value safely — no error — when the key is missing. Use bracket
access when a key is guaranteed to be there; use <code>.get()</code> with
a sensible default whenever it might not be, which is common when working
with data that came from an external source like an API response.</p>
""",
    },
]


def deepen_python_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="python")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0032_deepen_nextjs_content"),
    ]

    operations = [
        migrations.RunPython(deepen_python_content, noop),
    ]
