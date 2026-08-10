from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A client-optimized language from Google, best known as Flutter's language — and why learning it here pays off if you continue into Flutter.",
        "body": """
<p>Dart is a language built by Google for building fast apps on any
platform — it's best known today as the language Flutter apps are
written in. Its syntax will feel familiar if you've used Java, JavaScript,
or C#.</p>

<h2>Example: a minimal Dart program</h2>
<pre><code>void main() {
  print('Hello, world!');
}</code></pre>
<pre><code>Hello, world!</code></pre>
<p>Every Dart program starts execution from a <code>main()</code>
function — no wrapping class required, unlike Java or C#, which is one
small but real difference even though Dart's overall style leans
C-family. If you continue into the Flutter subject after this one,
everything you learn here about variables, functions, and classes
transfers directly, since Flutter code <em>is</em> Dart code.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "var, final, and const — three ways to declare a variable, each with a different promise about whether it can change.",
        "body": """
<p>Declare a variable with <code>var</code> and Dart infers its type
from the assigned value.</p>

<h2>Example: the three declaration keywords</h2>
<pre><code>void main() {
  var name = 'Ada';       // type inferred, can be reassigned
  final age = 21;          // set once, never reassigned
  const pi = 3.14159;      // a true compile-time constant
  print('$name is $age years old.');
}</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>Use <code>final</code> for a value that's set once and never
reassigned after that (common for something computed at runtime, like a
result from an API call). Use <code>const</code> specifically for a
value known and fixed at compile time — a genuine constant, not just "I
don't plan to change this." In practice, prefer <code>final</code> by
default for anything that won't be reassigned, and reach for
<code>var</code> only when a variable genuinely needs to change later.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — the familiar C-family set once again.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison
(<code>== != &gt; &lt;</code>), and logical
(<code>&amp;&amp; || !</code>) operators all work as you'd expect from
other C-family languages.</p>

<h2>Example: a boolean expression, printed with interpolation</h2>
<pre><code>void main() {
  int score = 85;
  bool passed = score >= 50 && score <= 100;
  print('Passed: $passed');
}</code></pre>
<pre><code>Passed: true</code></pre>
<p><code>$passed</code> inside a single-quoted string interpolates the
variable directly — Dart's string interpolation works in both single and
double-quoted strings, unlike some languages (PHP, for instance, only
interpolates inside double quotes).</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, else if, and else — familiar structure once more.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> work the
same as in Java, JavaScript, or C#.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>void main() {
  int hour = 14;
  String greeting;

  if (hour < 12) {
    greeting = 'Good morning';
  } else if (hour < 18) {
    greeting = 'Good afternoon';
  } else {
    greeting = 'Good evening';
  }

  print(greeting);
}</code></pre>
<pre><code>Good afternoon</code></pre>
<p>By now this exact structure should be recognizable from several other
subjects in this tutorial — that's a genuinely useful thing to notice:
across nearly every mainstream language, <code>if</code>/<code>else if</code>/<code>else</code>
branching is close to identical, so it's one of the fastest concepts to
transfer once you've truly learned it in any single language.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for and while — plus the for-in form for stepping through a list.",
        "body": """
<p>Dart's <code>for</code> loop uses the familiar three-part structure.
There's also a <code>for-in</code> form for stepping through every item
in a list without managing an index yourself.</p>

<h2>Example: a standard for loop</h2>
<pre><code>void main() {
  var total = 0;
  for (var i = 1; i <= 5; i++) {
    total += i;
  }
  print('Total: $total');
}</code></pre>
<pre><code>Total: 15</code></pre>
<p>You'll meet <code>for-in</code> properly in the Lists lesson next —
it plays the same role as Java's enhanced for-loop, C#'s
<code>foreach</code>, and PHP's <code>foreach</code>: stepping through
each value directly, with no manual index bookkeeping.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Reusable blocks of code, with an optional return type — and the short arrow syntax for one-line functions.",
        "body": """
<p>Define a function with a return type, name, and parameters:
<code>String greet(String name) { ... }</code>.</p>

<h2>Example: a regular function and the arrow shorthand</h2>
<pre><code>String greet(String name) {
  return 'Hello, $name!';
}

int square(int n) => n * n;

void main() {
  print(greet('Chidi'));
  print('Square of 6 is ${square(6)}');
}</code></pre>
<pre><code>Hello, Chidi!
Square of 6 is 36</code></pre>
<p><code>int square(int n) => n * n;</code> is Dart's short arrow syntax
for a one-line function that immediately returns an expression — no
curly braces or explicit <code>return</code> needed. It's purely a
shorthand for the exact same thing as the longer <code>greet</code>
function above; reach for it whenever a function's whole body is one
simple expression.</p>
""",
    },
    {
        "slug": "lists",
        "summary": "Ordered collections, similar to arrays in other languages, and the map() method for transforming one into another.",
        "body": """
<p>A <code>List</code> holds an ordered collection of values:
<code>var numbers = [1, 2, 3, 4, 5];</code>.</p>

<h2>Example: transforming a list with map()</h2>
<pre><code>void main() {
  var numbers = [1, 2, 3, 4, 5];
  var doubled = numbers.map((n) => n * 2).toList();
  print(doubled);
}</code></pre>
<pre><code>[2, 4, 6, 8, 10]</code></pre>
<p><code>.map()</code> transforms every item using the function you pass
it — here, the arrow function from the previous lesson — and returns a
new, lazily-evaluated sequence, which <code>.toList()</code> then
converts into a real, concrete list. This is the same underlying idea as
JavaScript's <code>.map()</code> array method, just Dart's particular
spelling of it (with that extra <code>.toList()</code> step Dart requires
that JavaScript doesn't).</p>
""",
    },
    {
        "slug": "classes-and-objects",
        "summary": "Blueprints (classes) and the instances made from them — and why this pattern matters even more once you move on to Flutter.",
        "body": """
<p>A class describes fields and methods; <code>ClassName(...)</code>
creates an object from it — Dart doesn't require the <code>new</code>
keyword, unlike Java or C#.</p>

<h2>Example: a Student class</h2>
<pre><code>class Student {
  String name;
  String track;

  Student(this.name, this.track);
}

void main() {
  var ada = Student('Ada', 'Frontend');
  print('${ada.name} is studying ${ada.track}');
}</code></pre>
<pre><code>Ada is studying Frontend</code></pre>
<p><code>Student(this.name, this.track);</code> is Dart's compact
constructor shorthand — <code>this.name</code> directly assigns the
constructor's first argument to the object's own <code>name</code> field,
with no separate assignment line needed inside the constructor body, the
way Java or C# would require. This exact same "class describes a blueprint,
new instances get created from it" pattern is precisely how Flutter builds
every single UI widget — which is exactly why learning Dart's classes
first makes Flutter's structure click much faster.</p>
""",
    },
]


def deepen_dart_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="dart")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0040_deepen_csharp_content"),
    ]

    operations = [
        migrations.RunPython(deepen_dart_content, noop),
    ]
