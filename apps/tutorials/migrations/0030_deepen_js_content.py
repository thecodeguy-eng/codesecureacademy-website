from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "What JavaScript does, how it runs inside a page, and why these examples write to the page instead of a console.",
        "body": """
<p>HTML structures a page and CSS styles it; JavaScript makes it
<em>interactive</em> — responding to clicks, updating content without
reloading, validating forms, fetching new data. It runs inside a
<code>&lt;script&gt;</code> tag, either directly in the page or linked
from a separate <code>.js</code> file.</p>

<h2>Example: writing output onto the page</h2>
<pre><code>&lt;p id="output"&gt;Loading...&lt;/p&gt;

&lt;script&gt;
  document.getElementById("output").textContent = "Hello from JavaScript!";
&lt;/script&gt;</code></pre>
<p>Since there's no visible browser console in this preview,
<code>document.getElementById(...)</code> finds an element already on the
page by its <code>id</code>, and setting <code>.textContent</code>
replaces whatever text is inside it. Every example in this tutorial
follows this same pattern: find something on the page, change it — which
is, at its core, most of what JavaScript is actually used for on a real
site.</p>
""",
    },
    {
        "slug": "variables",
        "summary": "Storing values with let and const — and why const should be your default, not let.",
        "body": """
<p><code>let</code> declares a variable you can reassign later.
<code>const</code> declares one that can't be reassigned after its first
value. <code>var</code> is an older way to declare variables with looser,
more error-prone rules — modern JavaScript avoids it almost entirely.</p>

<h2>Example: const by default, let only when needed</h2>
<pre><code>const name = "Ada";     // never reassigned — use const
let age = 21;            // will change below — needs let
age = age + 1;

document.getElementById("output").textContent = name + " is now " + age;</code></pre>
<p>Reach for <code>const</code> by default, and switch to
<code>let</code> only once you know a value genuinely needs to change
later. This isn't just a style preference — a <code>const</code> that
someone later tries to reassign throws an immediate error, catching a
whole class of accidental-reassignment bugs the moment they happen,
rather than silently letting a value change somewhere unexpected.</p>
""",
    },
    {
        "slug": "data-types",
        "summary": "Strings, numbers, booleans, arrays, and objects — the handful of types nearly everything in JavaScript is built from.",
        "body": """
<p>JavaScript's core types: <strong>string</strong> (text, in quotes),
<strong>number</strong> (JavaScript uses one type for both whole numbers
and decimals — no separate "integer" type), <strong>boolean</strong>
(<code>true</code> or <code>false</code>), <strong>array</strong> (an
ordered list), and <strong>object</strong> (key/value pairs).</p>

<h2>Example: checking a value's type</h2>
<pre><code>const text = "hello";
const count = 42;
const isReady = true;

document.getElementById("output").textContent =
  typeof text + ", " + typeof count + ", " + typeof isReady;</code></pre>
<p><code>typeof</code> tells you a value's type at runtime — genuinely
useful when a value's type isn't obvious just from reading the code, like
data that just arrived from an API response. Try changing
<code>count</code> to a string like <code>"42"</code> in the editor and
notice how <code>typeof</code> now reports <code>"string"</code> — a
subtle but real difference that trips up a lot of beginners comparing
"42" to 42 later on.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — and why === beats == almost every time.",
        "body": """
<p>Arithmetic operators (<code>+ - * / %</code>) do math. Comparison
operators (<code>=== !== &gt; &lt;</code>) compare two values and
produce a boolean.</p>

<h2>Example: why === and not ==</h2>
<pre><code>console_check_1 = (0 == "");    // true  — surprising!
console_check_2 = (0 === "");   // false — no automatic conversion

const score = 85;
const passed = score >= 50 && score <= 100;
document.getElementById("output").textContent = "Passed: " + passed;</code></pre>
<p><code>==</code> ("loose equality") silently converts values to a
matching type before comparing them, which produces surprising results
like the first line above. <code>===</code> ("strict equality") skips
that conversion entirely — it compares both value <em>and</em> type,
which is almost always what you actually mean. Use <code>===</code> and
<code>!==</code> by default; reach for <code>==</code> only if you can
explain exactly why you need the automatic conversion.</p>

<h2>Combining conditions with logical operators</h2>
<p><code>&amp;&amp;</code> ("and") requires both sides to be true;
<code>||</code> ("or") requires at least one; <code>!</code> negates a
single value. The example above uses <code>&amp;&amp;</code> to check
that a score is <em>both</em> at least 50 <em>and</em> at most 100.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching logic with if, else if, and else — the exact pattern that decides which path code takes.",
        "body": """
<p><code>if</code> runs a block only when its condition is true. Add
<code>else if</code> for another condition to check if the first was
false, and a final <code>else</code> to catch everything else.</p>

<h2>Example: a greeting that depends on the time of day</h2>
<pre><code>const hour = 14;
let greeting;

if (hour < 12) {
  greeting = "Good morning";
} else if (hour < 18) {
  greeting = "Good afternoon";
} else {
  greeting = "Good evening";
}

document.getElementById("output").textContent = greeting;</code></pre>
<p>JavaScript checks each condition top to bottom and stops at the first
one that's true — so even though <code>hour &lt; 18</code> would also be
true for an hour of 9, it never gets checked because
<code>hour &lt; 12</code> already matched first. Order matters: put your
most specific conditions before more general ones that would also match.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for loops and while loops — and when to reach for each one.",
        "body": """
<p>A <code>for</code> loop repeats a block a set number of times —
useful when you know how many iterations you need, like stepping through
an array. A <code>while</code> loop repeats as long as a condition stays
true — useful when you don't know the count in advance.</p>

<h2>Example 1: for — a known number of steps</h2>
<pre><code>let result = "";
for (let i = 1; i <= 5; i++) {
  result += i + " ";
}
document.getElementById("output").textContent = "Counted: " + result;</code></pre>
<p>The three parts inside the parentheses run in a fixed order: the
starting value (<code>let i = 1</code>) runs once, the condition
(<code>i &lt;= 5</code>) is checked before every loop, and the update
(<code>i++</code>) runs after every loop — this exact three-part shape is
one of the most common patterns you'll write in any C-family language,
not just JavaScript.</p>

<h2>Example 2: while — an unknown number of steps</h2>
<pre><code>let total = 0;
let n = 1;
while (total < 20) {
  total += n;
  n++;
}
document.getElementById("output").textContent = "Total reached: " + total;</code></pre>
<p>Here we don't know in advance how many additions it'll take to reach
20 — <code>while</code> is the right tool exactly when the stopping
condition depends on something computed as you go, not a fixed count you
already know.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Packaging reusable logic with function declarations and arrow functions — two syntaxes, the same underlying idea.",
        "body": """
<p>A function is a reusable block of code. Define it once, then
<strong>call</strong> it by name wherever you need it, passing different
arguments each time.</p>

<h2>Example 1: a standard function declaration</h2>
<pre><code>function greet(name) {
  return "Hello, " + name + "!";
}

document.getElementById("output").textContent = greet("Chidi");</code></pre>
<p><code>return</code> sends a value back out of the function to wherever
it was called from — without it, calling <code>greet("Chidi")</code>
would still run the code inside, but the result would be
<code>undefined</code> everywhere else.</p>

<h2>Example 2: the shorter arrow function syntax</h2>
<pre><code>const square = (n) => n * n;
const greetArrow = (name) => "Hi, " + name + "!";

document.getElementById("output").textContent =
  greetArrow("Ada") + " Square of 6 is " + square(6);</code></pre>
<p>Arrow functions are a more compact syntax for the same idea — a
one-line arrow function with no curly braces automatically returns its
expression, no explicit <code>return</code> keyword needed. You'll see
arrow functions constantly in modern JavaScript, especially for short
functions passed as arguments to other functions, which the Arrays lesson
shows next.</p>
""",
    },
    {
        "slug": "arrays",
        "summary": "Ordered lists of values, and the methods to work with them — map and filter especially.",
        "body": """
<p>An array holds an ordered list of values in square brackets:
<code>const fruits = ["apple", "banana"]</code>. Access items by their
zero-based index (<code>fruits[0]</code> is <code>"apple"</code>).</p>

<h2>Example: map and filter, the two most-used array methods</h2>
<pre><code>const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map((n) => n * 2);
const evens = numbers.filter((n) => n % 2 === 0);

document.getElementById("output").textContent =
  "Doubled: " + doubled.join(", ") + " | Evens: " + evens.join(", ");</code></pre>
<p><code>.map()</code> transforms every item into something new and
returns a brand-new array of the same length — here, each number becomes
double itself. <code>.filter()</code> keeps only the items where the
given function returns true, discarding the rest — here, only the even
numbers survive. Neither method changes the original <code>numbers</code>
array at all; both return a completely new one, which is a deliberate
JavaScript convention worth internalizing early, since it avoids a whole
category of bugs where code accidentally mutates data something else is
still relying on.</p>
""",
    },
    {
        "slug": "objects",
        "summary": "Grouping related data as key/value pairs — and the two ways to read a value back out.",
        "body": """
<p>An object groups related values under named keys:
<code>const user = { name: "Ada", age: 21 }</code>.</p>

<h2>Example: dot notation vs. bracket notation</h2>
<pre><code>const student = {
  name: "Ada",
  track: "Frontend",
  isEnrolled: true,
};

document.getElementById("output").textContent =
  student.name + " is studying " + student["track"];</code></pre>
<p><code>student.name</code> (dot notation) and
<code>student["track"]</code> (bracket notation) both read the same kind
of value — the difference is that bracket notation lets the key itself be
a variable, computed at runtime:
<code>const key = "track"; student[key]</code> works, while
<code>student.key</code> would look for a literal property named
<code>"key"</code>, which doesn't exist. Use dot notation by default;
switch to bracket notation only when the property name needs to be
dynamic.</p>
""",
    },
    {
        "slug": "dom-manipulation",
        "summary": "Reading and changing the page itself with document methods — how JavaScript actually makes a static page interactive.",
        "body": """
<p>The DOM (Document Object Model) is the browser's live, in-memory
representation of the page. <code>document.getElementById()</code> finds
an element; once you have it, you can change its content, its style, or
attach an event listener so it reacts to user interaction.</p>

<h2>Example: a counter that reacts to clicks</h2>
<pre><code>&lt;button id="btn"&gt;Click me&lt;/button&gt;
&lt;p id="output"&gt;Button not clicked yet.&lt;/p&gt;

&lt;script&gt;
  let clicks = 0;
  document.getElementById("btn").addEventListener("click", function () {
    clicks++;
    document.getElementById("output").textContent = "Clicked " + clicks + " time(s).";
  });
&lt;/script&gt;</code></pre>
<p><code>.addEventListener("click", ...)</code> attaches a function that
runs every time that specific element is clicked — nothing happens until
the click actually occurs; the function just waits, registered and ready.
This is the fundamental mechanism behind essentially every interactive
element on the web: a listener waiting for an event, and a function that
runs in response to update the page. Everything from a "like" button to a
full single-page app is built from more elaborate versions of this exact
same pattern.</p>
""",
    },
]


def deepen_js_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="javascript")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0029_deepen_css_content"),
    ]

    operations = [
        migrations.RunPython(deepen_js_content, noop),
    ]
