from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A server-side language that runs before the page reaches the browser — and why that matters for what PHP can and can't do.",
        "body": """
<p>PHP runs on the <em>server</em>, not in the browser — it generates
HTML which then gets sent to the visitor, who never sees the PHP code
itself, only its output. It powers a huge share of the web (WordPress,
for one).</p>

<h2>Example: the basic syntax</h2>
<pre><code>&lt;?php
  echo "Hello, world!";
?&gt;</code></pre>
<pre><code>Hello, world!</code></pre>
<p>PHP code lives between <code>&lt;?php</code> and <code>?&gt;</code>
tags — everything outside those tags is treated as plain HTML and passed
through untouched, which is why PHP files commonly mix real HTML markup
with chunks of PHP logic in the same file. <code>echo</code> outputs
text, and statements end with a semicolon.</p>
""",
    },
    {
        "slug": "variables",
        "summary": "PHP variables always start with a dollar sign, and don't need a declared type.",
        "body": """
<p>Every PHP variable name starts with <code>$</code>:
<code>$name = "Ada";</code>. Like Python or JavaScript, you don't declare
a type — it's inferred from whatever value you assign.</p>

<h2>Example: variables inside a string</h2>
<pre><code>&lt;?php
  $name = "Ada";
  $age = 21;
  echo "$name is $age years old.";
?&gt;</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>Variables placed directly inside a double-quoted string
(<code>"$name"</code>) are automatically substituted with their value —
this only works inside <strong>double</strong> quotes; single-quoted
strings (<code>'$name'</code>) print the literal text <code>$name</code>
instead, with no substitution at all. That distinction catches a lot of
beginners the first time they switch quote styles without thinking about
it.</p>
""",
    },
    {
        "slug": "echo-and-concatenation",
        "summary": "Joining strings together with the dot operator — PHP's own way of building combined output.",
        "body": """
<p><code>echo</code> can print several things separated by commas, or you
can join (<strong>concatenate</strong>) strings into one using the
<code>.</code> operator.</p>

<h2>Example: building a full name</h2>
<pre><code>&lt;?php
  $first = "Chi";
  $last = "nedu";
  echo $first . $last;
?&gt;</code></pre>
<pre><code>Chinedu</code></pre>
<p>PHP uses <code>.</code> for string concatenation — worth noting
explicitly, since many other languages (JavaScript, Python) reuse
<code>+</code> for the same job, and reaching for <code>+</code> out of
habit in PHP does something entirely different (numeric addition, which
usually produces an unexpected result or a warning when applied to text).</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — including the stricter three-equals comparison.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>) and logical (<code>&amp;&amp; || !</code>)
operators work much like other C-family languages.</p>

<h2>Example: loose vs. strict comparison</h2>
<pre><code>&lt;?php
  $score = 85;
  $passed = $score >= 50 && $score <= 100;
  echo $passed ? "true" : "false";
?&gt;</code></pre>
<pre><code>true</code></pre>
<p>PHP offers both <code>==</code> (loose — allows type conversion before
comparing, similar to JavaScript's <code>==</code>) and
<code>===</code> (strict — compares type and value together, no
conversion). As with JavaScript, prefer <code>===</code> by default; it
avoids surprising results like <code>0 == "abc"</code> historically
returning true in some PHP versions.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, elseif, and else — familiar C-family syntax with curly braces.",
        "body": """
<p><code>if</code>, <code>elseif</code>, and <code>else</code> work the
same as most C-family languages — each block wrapped in curly braces,
condition in parentheses.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>&lt;?php
  $hour = 14;

  if ($hour < 12) {
    echo "Good morning";
  } elseif ($hour < 18) {
    echo "Good afternoon";
  } else {
    echo "Good evening";
  }
?&gt;</code></pre>
<pre><code>Good afternoon</code></pre>
<p>Note the spelling: PHP uses <code>elseif</code> as one word (though
<code>else if</code> as two words also works) — a small but real
difference from JavaScript's <code>else if</code>, worth knowing so it
doesn't trip you up switching between languages.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for, while, and foreach — PHP's dedicated tool for stepping through arrays.",
        "body": """
<p><code>for</code> and <code>while</code> loops work like most
C-family languages. <code>foreach</code> is PHP's dedicated way to step
through every item in an array without managing an index yourself.</p>

<h2>Example: for vs. foreach</h2>
<pre><code>&lt;?php
  $total = 0;
  for ($i = 1; $i <= 5; $i++) {
    $total += $i;
  }
  echo "Total: $total";
?&gt;</code></pre>
<pre><code>Total: 15</code></pre>
<p><code>for</code> is the right tool when you need the index itself
(counting, or accessing items by position); <code>foreach</code>, covered
properly in the Arrays lesson next, is the right tool the moment you just
need each value in turn and don't care about tracking a numeric index —
which describes most real loops over array data.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Defining reusable logic with the function keyword.",
        "body": """
<p>Define a function with <code>function name($params) { ... }</code>,
and <code>return</code> a value if it should produce one.</p>

<h2>Example: a greeting function</h2>
<pre><code>&lt;?php
  function greet($name) {
    return "Hello, $name!";
  }

  echo greet("Chidi");
?&gt;</code></pre>
<pre><code>Hello, Chidi!</code></pre>
<p>Note that variables interpolate inside the returned string exactly the
same way they did in the Echo lesson — <code>$name</code> works inside a
double-quoted string whether it's a top-level variable or, as here, a
function parameter.</p>
""",
    },
    {
        "slug": "arrays",
        "summary": "Indexed and associative arrays, and how foreach steps through either kind.",
        "body": """
<p>A regular (indexed) array is a numbered list:
<code>$fruits = ["apple", "banana"]</code>. An
<strong>associative</strong> array uses named keys instead of numbers.</p>

<h2>Example: an associative array and foreach</h2>
<pre><code>&lt;?php
  $student = ["name" => "Ada", "track" => "Frontend"];
  echo $student["name"] . " is studying " . $student["track"];

  foreach ($student as $key => $value) {
    echo "$key: $value\\n";
  }
?&gt;</code></pre>
<pre><code>Ada is studying Frontend
name: Ada
track: Frontend</code></pre>
<p><code>=&gt;</code> pairs a key with its value when building an
associative array. <code>foreach ($student as $key => $value)</code>
steps through every key/value pair at once — for a plain indexed array,
you'd instead write <code>foreach ($fruits as $fruit)</code>, dropping
the key since a numeric index usually isn't meaningful on its own.</p>
""",
    },
]


def deepen_php_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="php")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0033_deepen_python_content"),
    ]

    operations = [
        migrations.RunPython(deepen_php_content, noop),
    ]
