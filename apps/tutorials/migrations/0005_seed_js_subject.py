from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to JavaScript",
        "slug": "introduction",
        "order": 1,
        "summary": "What JavaScript does, and how to run it inside a page.",
        "body": """
<p>HTML structures a page and CSS styles it; JavaScript makes it <em>interactive</em> &mdash;
responding to clicks, updating content without reloading, validating forms, and more. It
runs inside a <code>&lt;script&gt;</code> tag, either in the page's head/body or linked from
a separate <code>.js</code> file.</p>
<p>Since there's no visible console in this preview, these examples write their results onto
the page itself using <code>document.getElementById(...)</code>.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <h1>JavaScript Demo</h1>
  <p id="output">Loading...</p>

  <script>
    document.getElementById("output").textContent = "Hello from JavaScript!";
  </script>

</body>
</html>
""",
    },
    {
        "title": "Variables (let, const, var)",
        "slug": "variables",
        "order": 2,
        "summary": "Storing values with let and const, and why var is mostly avoided now.",
        "body": """
<p><code>let</code> declares a variable you can reassign later. <code>const</code>
declares one that can't be reassigned after its first value &mdash; use it by default, and
switch to <code>let</code> only when you know the value needs to change. <code>var</code> is
an older way to declare variables with looser rules; modern JavaScript avoids it in favour of
<code>let</code>/<code>const</code>.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const name = "Ada";
    let age = 21;
    age = age + 1; // let can be reassigned

    document.getElementById("output").textContent = name + " is now " + age + " years old.";
  </script>

</body>
</html>
""",
    },
    {
        "title": "Data Types",
        "slug": "data-types",
        "order": 3,
        "summary": "Strings, numbers, booleans, arrays, and objects.",
        "body": """
<p>JavaScript's core types: <strong>string</strong> (text, in quotes), <strong>number</strong>
(no separate type for whole vs. decimal numbers), <strong>boolean</strong> (<code>true</code>
or <code>false</code>), <strong>array</strong> (an ordered list), and <strong>object</strong>
(key/value pairs). <code>typeof</code> tells you what type a value is.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const text = "hello";
    const count = 42;
    const isReady = true;

    document.getElementById("output").textContent =
      typeof text + ", " + typeof count + ", " + typeof isReady;
  </script>

</body>
</html>
""",
    },
    {
        "title": "Operators",
        "slug": "operators",
        "order": 4,
        "summary": "Arithmetic, comparison, and logical operators.",
        "body": """
<p>Arithmetic operators (<code>+ - * / %</code>) do math. Comparison operators
(<code>=== !== &gt; &lt;</code>) compare two values and produce a boolean. Use
<code>===</code> (strict equality) rather than <code>==</code> &mdash; it compares type as
well as value, avoiding surprising automatic conversions. Logical operators
(<code>&& || !</code>) combine boolean conditions.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const score = 85;
    const passed = score >= 50 && score <= 100;

    document.getElementById("output").textContent = "Passed: " + passed;
  </script>

</body>
</html>
""",
    },
    {
        "title": "Conditionals (if / else)",
        "slug": "conditionals",
        "order": 5,
        "summary": "Branching logic with if, else if, and else.",
        "body": """
<p><code>if</code> runs a block only when its condition is true. Add <code>else if</code>
for another condition to check if the first was false, and a final <code>else</code> to
catch everything else.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const hour = 14;
    let greeting;

    if (hour < 12) {
      greeting = "Good morning";
    } else if (hour < 18) {
      greeting = "Good afternoon";
    } else {
      greeting = "Good evening";
    }

    document.getElementById("output").textContent = greeting;
  </script>

</body>
</html>
""",
    },
    {
        "title": "Loops (for / while)",
        "slug": "loops",
        "order": 6,
        "summary": "Repeating code with for loops and while loops.",
        "body": """
<p>A <code>for</code> loop repeats a block a set number of times &mdash; useful when you
know how many iterations you need, like stepping through an array. A <code>while</code>
loop repeats as long as a condition stays true &mdash; useful when you don't know the count
in advance.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    let result = "";
    for (let i = 1; i <= 5; i++) {
      result += i + " ";
    }

    document.getElementById("output").textContent = "Counted: " + result;
  </script>

</body>
</html>
""",
    },
    {
        "title": "Functions",
        "slug": "functions",
        "order": 7,
        "summary": "Packaging reusable logic with function declarations and arrow functions.",
        "body": """
<p>A function is a reusable block of code. Define it once with <code>function name(...)</code>
(or the shorter arrow syntax <code>const name = (...) =&gt; {...}</code>), then
<strong>call</strong> it by name wherever you need it, passing different arguments each time.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    function greet(name) {
      return "Hello, " + name + "!";
    }

    const square = (n) => n * n;

    document.getElementById("output").textContent = greet("Chidi") + " Square of 6 is " + square(6);
  </script>

</body>
</html>
""",
    },
    {
        "title": "Arrays",
        "slug": "arrays",
        "order": 8,
        "summary": "Ordered lists of values, and the methods to work with them.",
        "body": """
<p>An array holds an ordered list of values in square brackets:
<code>const fruits = ["apple", "banana"]</code>. Access items by their zero-based index
(<code>fruits[0]</code>), and use methods like <code>.push()</code> to add,
<code>.map()</code> to transform every item, and <code>.filter()</code> to keep only items
matching a condition.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const numbers = [1, 2, 3, 4, 5];
    const doubled = numbers.map((n) => n * 2);
    const evens = numbers.filter((n) => n % 2 === 0);

    document.getElementById("output").textContent =
      "Doubled: " + doubled.join(", ") + " | Evens: " + evens.join(", ");
  </script>

</body>
</html>
""",
    },
    {
        "title": "Objects",
        "slug": "objects",
        "order": 9,
        "summary": "Grouping related data as key/value pairs.",
        "body": """
<p>An object groups related values under named keys:
<code>const user = { name: "Ada", age: 21 }</code>. Access a value with dot notation
(<code>user.name</code>) or bracket notation (<code>user["name"]</code>) &mdash; bracket
notation is handy when the key name is itself stored in a variable.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p id="output"></p>

  <script>
    const student = {
      name: "Ada",
      track: "Frontend",
      isEnrolled: true,
    };

    document.getElementById("output").textContent =
      student.name + " is studying " + student.track;
  </script>

</body>
</html>
""",
    },
    {
        "title": "DOM Manipulation",
        "slug": "dom-manipulation",
        "order": 10,
        "summary": "Reading and changing the page itself with document methods.",
        "body": """
<p>The DOM (Document Object Model) is the browser's live representation of the page.
<code>document.getElementById()</code> (or <code>querySelector()</code>) finds an element;
once you have it, you can change its <code>.textContent</code>, its <code>.style</code>, or
attach an event listener so it reacts to clicks. This is how JavaScript makes a static page
interactive.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <button id="btn">Click me</button>
  <p id="output">Button not clicked yet.</p>

  <script>
    let clicks = 0;
    document.getElementById("btn").addEventListener("click", function () {
      clicks++;
      document.getElementById("output").textContent = "Clicked " + clicks + " time(s).";
    });
  </script>

</body>
</html>
""",
    },
]


def seed_js_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="javascript",
        defaults={
            "name": "JavaScript",
            "icon": "⚡",
            "description": "The programming language that makes web pages interactive.",
            "editor_language": "js",
            "order": 3,
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
            },
        )


def unseed_js_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="javascript").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0004_seed_css_subject"),
    ]

    operations = [
        migrations.RunPython(seed_js_subject, unseed_js_subject),
    ]
