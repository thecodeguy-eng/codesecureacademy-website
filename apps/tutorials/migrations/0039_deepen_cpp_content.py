from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A fast, compiled language that gives you close control over memory — and why that control is both its strength and its risk.",
        "body": """
<p>C++ compiles down to machine code and gives you fine control over
memory and performance — it's used for games, operating systems, and
other performance-critical software where every millisecond and every
byte genuinely matters.</p>

<h2>Example: a minimal C++ program</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int main() {
    cout << "Hello, world!" << endl;
    return 0;
}</code></pre>
<pre><code>Hello, world!</code></pre>
<p><code>#include &lt;iostream&gt;</code> pulls in the input/output
library so <code>cout</code> (console output) is available.
<code>&lt;&lt;</code> "sends" a value to <code>cout</code> to be
printed, and <code>return 0;</code> tells the operating system the
program finished successfully — a nonzero return would signal an error
occurred, a convention this language shares with C and most command-line
tools.</p>
""",
    },
    {
        "slug": "variables-and-data-types",
        "summary": "Declaring typed variables — int, double, bool, string, each with an explicit type like Java.",
        "body": """
<p>Like Java, C++ variables need an explicit type:
<code>int age = 21;</code>.</p>

<h2>Example: string, int, and output together</h2>
<pre><code>#include &lt;iostream&gt;
#include &lt;string&gt;
using namespace std;

int main() {
    string name = "Ada";
    int age = 21;
    cout << name << " is " << age << " years old." << endl;
    return 0;
}</code></pre>
<pre><code>Ada is 21 years old.</code></pre>
<p>Common types: <code>int</code>, <code>double</code>,
<code>bool</code>, and <code>string</code> (from the
<code>&lt;string&gt;</code> header — notice it needs its own separate
include, unlike <code>iostream</code>). Chaining multiple
<code>&lt;&lt;</code> together, as above, is the standard C++ way to
build up a printed line from several separate pieces.</p>
""",
    },
    {
        "slug": "operators",
        "summary": "Arithmetic, comparison, and logical operators — familiar C-family syntax.",
        "body": """
<p>Arithmetic (<code>+ - * /</code>), comparison
(<code>== != &gt; &lt;</code>), and logical
(<code>&amp;&amp; || !</code>) operators work as in most C-family
languages.</p>

<h2>Example: a boolean expression and a ternary for output</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int main() {
    int score = 85;
    bool passed = score >= 50 && score <= 100;
    cout << "Passed: " << (passed ? "true" : "false") << endl;
    return 0;
}</code></pre>
<pre><code>Passed: true</code></pre>
<p>C++ doesn't have a genuine boolean-to-string conversion built in the
way some languages do — printing <code>passed</code> directly would show
<code>1</code> or <code>0</code>, not the word "true" or "false" — so the
ternary <code>(passed ? "true" : "false")</code> is a common, idiomatic
way to print a readable label instead.</p>
""",
    },
    {
        "slug": "conditionals",
        "summary": "Branching with if, else if, and else — the same structure Java and C# share.",
        "body": """
<p><code>if</code>, <code>else if</code>, and <code>else</code> behave
the same as in Java or JavaScript.</p>

<h2>Example: a time-of-day greeting</h2>
<pre><code>#include &lt;iostream&gt;
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
}</code></pre>
<pre><code>Good afternoon</code></pre>
<p>If you've already read the Java tutorial's conditionals lesson, this
should look almost identical — that's exactly the point of a shared
"C-family" syntax: once you know the pattern in one of these languages,
recognizing it in another is mostly about spotting small syntax
differences, not relearning the underlying logic from scratch.</p>
""",
    },
    {
        "slug": "loops",
        "summary": "Repeating code with for and while — the same three-part structure as Java and JavaScript.",
        "body": """
<p>C++'s <code>for</code> loop follows the same three-part structure as
Java and JavaScript: initializer, condition, update.</p>

<h2>Example: summing with a for loop</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int main() {
    int total = 0;
    for (int i = 1; i <= 5; i++) {
        total += i;
    }
    cout << "Total: " << total << endl;
    return 0;
}</code></pre>
<pre><code>Total: 15</code></pre>
<p>Same shape, same result as the Java and JavaScript versions of this
exact example elsewhere in this tutorial — worth comparing them side by
side if you're learning more than one language, since the differences
that remain (semicolons, <code>cout</code> vs. <code>print</code>,
header includes) are genuinely small once the core loop logic is already
familiar.</p>
""",
    },
    {
        "slug": "functions",
        "summary": "Reusable blocks of code with a declared return type — and why declaring one before main() matters here.",
        "body": """
<p>A function declares its return type, name, and parameter types up
front: <code>int add(int a, int b) { ... }</code>.</p>

<h2>Example: a function used before main()</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int square(int n) {
    return n * n;
}

int main() {
    cout << "Square of 6 is " << square(6) << endl;
    return 0;
}</code></pre>
<pre><code>Square of 6 is 36</code></pre>
<p>Unlike some languages, C++ generally requires a function to be
declared (or at least its signature known) before the point where it's
called — here, <code>square</code> is defined entirely above
<code>main</code>, so by the time <code>main</code> calls it, the
compiler already knows exactly what <code>square</code> looks like. Use
<code>void</code> as the return type for a function that doesn't return a
value at all.</p>
""",
    },
    {
        "slug": "arrays",
        "summary": "Fixed-size, single-type collections — and why, unlike Java, C++ arrays don't track their own length.",
        "body": """
<p>An array holds a fixed number of same-typed values:
<code>int numbers[5] = {1, 2, 3, 4, 5};</code>.</p>

<h2>Example: manually tracking the length</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int main() {
    int numbers[5] = {1, 2, 3, 4, 5};
    int total = 0;
    for (int i = 0; i < 5; i++) {
        total += numbers[i];
    }
    cout << "Total: " << total << endl;
    return 0;
}</code></pre>
<pre><code>Total: 15</code></pre>
<p>Notice the loop condition is hardcoded as <code>i &lt; 5</code>,
matching the array's known size. Unlike Java's <code>numbers.length</code>,
a plain C++ array doesn't know its own length at all — the size has to be
tracked separately by whoever's using it, which is exactly the kind of
manual bookkeeping that modern C++ code more often avoids with a
<code>std::vector</code> instead, a topic for a later lesson.</p>
""",
    },
    {
        "slug": "pointers",
        "summary": "Variables that store a memory address instead of a value — the idea underneath C++'s reputation for low-level control.",
        "body": """
<p>A pointer stores the memory <em>address</em> of another variable,
rather than a value directly.</p>

<h2>Example: a pointer to an int</h2>
<pre><code>#include &lt;iostream&gt;
using namespace std;

int main() {
    int age = 21;
    int* agePointer = &age;

    cout << "Value: " << *agePointer << endl;
    cout << "Address stored in pointer: " << agePointer << endl;
    return 0;
}</code></pre>
<pre><code>Value: 21
Address stored in pointer: 0x7ffeeb1c2a9c   (a real address differs every run)</code></pre>
<p>Declare a pointer with <code>*</code> (<code>int* agePointer;</code>),
and get a variable's address with <code>&amp;</code>. Writing
<code>*agePointer</code> (with the asterisk again) "follows" the pointer
back to the actual value it points at — this is called
<strong>dereferencing</strong>. Pointers are one of the things that give
C++ its low-level control, and also one of the things that make it easy
to make mistakes (following a pointer to memory that's no longer valid is
a classic, hard-to-debug C++ bug) — most modern C++ code prefers safer
alternatives like references and smart pointers where possible. This
lesson is just the basic idea the rest builds on.</p>
""",
    },
]


def deepen_cpp_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="cpp")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0038_deepen_java_content"),
    ]

    operations = [
        migrations.RunPython(deepen_cpp_content, noop),
    ]
