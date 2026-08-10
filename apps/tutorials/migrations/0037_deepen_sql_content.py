from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "How SQL talks to a database made of tables, rows, and columns — the students table every later lesson builds on.",
        "body": """
<p>SQL (Structured Query Language) is how you read and write data stored
in a relational database. Data lives in <strong>tables</strong> — think
of a table like a spreadsheet, with named <strong>columns</strong> and
one <strong>row</strong> per record.</p>

<h2>Example: the table every lesson in this tutorial reuses</h2>
<pre><code>SELECT * FROM students;</code></pre>
<pre><code>id | name  | track         | score
1  | Ada   | Frontend      | 92
2  | Chidi | Cybersecurity | 78
3  | Musa  | Backend       | 85</code></pre>
<p>Every example from here on queries this exact <code>students</code>
table — worth remembering its shape (four columns: id, name, track,
score), since later lessons will reference it without repeating the setup
each time.</p>
""",
    },
    {
        "slug": "select",
        "summary": "Choosing which columns to retrieve — the keyword that starts nearly every SQL query you'll ever write.",
        "body": """
<p><code>SELECT</code> picks which columns you want back.
<code>*</code> means "every column"; naming specific columns
(comma-separated) returns just those.</p>

<h2>Example: selecting specific columns</h2>
<pre><code>SELECT name, score FROM students;</code></pre>
<pre><code>name  | score
Ada   | 92
Chidi | 78
Musa  | 85</code></pre>
<p>Naming exact columns instead of always using <code>*</code> matters
for a real, practical reason once tables get wide — fetching only what
you actually need is faster, uses less memory, and makes it obvious to
anyone reading the query exactly what data it depends on.</p>
""",
    },
    {
        "slug": "where",
        "summary": "Filtering rows with a condition — and how AND/OR combine multiple conditions together.",
        "body": """
<p><code>WHERE</code> filters which rows come back, based on a
condition.</p>

<h2>Example: filtering with a condition</h2>
<pre><code>SELECT name, score FROM students WHERE score >= 85;</code></pre>
<pre><code>name | score
Ada  | 92
Musa | 85</code></pre>
<p>Combine multiple conditions with <code>AND</code> (both must be true)
or <code>OR</code> (at least one must be true) — for example,
<code>WHERE score >= 85 AND track = 'Frontend'</code> would narrow the
result down to just Ada, since Musa's track doesn't match even though
their score does.</p>
""",
    },
    {
        "slug": "order-by",
        "summary": "Sorting results ascending or descending — and the default you get if you forget to specify.",
        "body": """
<p><code>ORDER BY column</code> sorts the results. Add <code>DESC</code>
for descending order (highest/latest first).</p>

<h2>Example: highest score first</h2>
<pre><code>SELECT name, score FROM students ORDER BY score DESC;</code></pre>
<pre><code>name  | score
Ada   | 92
Musa  | 85
Chidi | 78</code></pre>
<p>Without <code>ORDER BY</code> at all, a database makes no promise
about what order rows come back in — it might happen to match insertion
order, or it might not, especially once a table has been updated many
times. Never rely on "the order it happens to return" without an explicit
<code>ORDER BY</code>; the default without it is ascending order
(<code>ASC</code>), which is why you only need to write <code>DESC</code>
explicitly, never <code>ASC</code>.</p>
""",
    },
    {
        "slug": "insert-into",
        "summary": "Adding a new row to a table — matching column names to values in the same order.",
        "body": """
<p><code>INSERT INTO table (columns) VALUES (values)</code> adds a new
row.</p>

<h2>Example: adding a new student</h2>
<pre><code>INSERT INTO students (name, track, score)
VALUES ('Ngozi', 'Frontend', 88);</code></pre>
<pre><code>1 row inserted.</code></pre>
<p>The columns listed and the values listed must match up in the exact
same order — here, <code>'Ngozi'</code> goes to <code>name</code>,
<code>'Frontend'</code> to <code>track</code>, <code>88</code> to
<code>score</code>. Notice <code>id</code> wasn't included at all — most
real tables auto-generate a new id for each inserted row, so you almost
never specify it yourself.</p>
""",
    },
    {
        "slug": "update-and-delete",
        "summary": "Changing existing rows, and removing them — and why the WHERE clause is the single most important part of both.",
        "body": """
<p><code>UPDATE table SET column = value WHERE condition</code> changes
existing rows. <code>DELETE FROM table WHERE condition</code> removes
rows the same way.</p>

<h2>Example: updating one specific row</h2>
<pre><code>UPDATE students SET score = 95 WHERE name = 'Chidi';</code></pre>
<pre><code>1 row updated.</code></pre>
<p>The <code>WHERE</code> clause here isn't optional in practice, even
though it's technically optional in syntax — leaving it off updates
<strong>every single row</strong> in the table, not just the one you
meant. This is one of the most common, most damaging mistakes anyone
makes with SQL, and it's worth developing the habit of writing and
double-checking your <code>WHERE</code> clause before you even glance at
the <code>SET</code> or the rest of the statement. The exact same warning
applies to <code>DELETE</code>, with even less room for a second chance.</p>
""",
    },
    {
        "slug": "join",
        "summary": "Combining rows from two related tables based on a matching column.",
        "body": """
<p>Real databases split data across multiple tables that reference each
other. A <code>JOIN</code> combines rows from two tables based on a
matching column.</p>

<h2>Example: joining students to their track's start date</h2>
<pre><code>SELECT students.name, tracks.start_date
FROM students
JOIN tracks ON students.track = tracks.name;</code></pre>
<pre><code>name  | start_date
Ada   | 2026-09-01
Chidi | 2026-10-15
Musa  | 2026-09-01</code></pre>
<p>Here, a separate <code>tracks</code> table stores each track's cohort
start date once; the <code>JOIN</code> matches each student's
<code>track</code> value to the corresponding row in <code>tracks</code>,
combining data from both tables into one result. This is the entire
reason relational databases split data across multiple tables in the
first place — instead of repeating "Frontend starts 2026-09-01" in every
single student row (and risking them drifting out of sync if that date
ever changes), it's stored once and joined in whenever it's actually
needed.</p>
""",
    },
    {
        "slug": "aggregate-functions",
        "summary": "COUNT, SUM, AVG, MIN, and MAX — summarizing many rows into one value, and how GROUP BY changes that from one summary to many.",
        "body": """
<p>Aggregate functions compute a single value across many rows:
<code>COUNT()</code> counts rows, <code>SUM()</code> totals a column,
<code>AVG()</code> averages it, <code>MIN()</code>/<code>MAX()</code>
find the smallest/largest value.</p>

<h2>Example: an average score per track</h2>
<pre><code>SELECT track, AVG(score) AS avg_score
FROM students
GROUP BY track;</code></pre>
<pre><code>track         | avg_score
Frontend      | 90.0
Cybersecurity | 78.0
Backend       | 85.0</code></pre>
<p>Without <code>GROUP BY</code>, <code>AVG(score)</code> alone would
collapse the <em>entire</em> table into one single average across every
student. Adding <code>GROUP BY track</code> changes that completely: it
computes a separate average for each distinct track value, producing one
row per group instead of one row total — the difference between "what's
the average score overall" and "what's the average score, broken down by
track," which is a genuinely different, much more useful question.</p>
""",
    },
]


def deepen_sql_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="sql")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0036_deepen_flask_content"),
    ]

    operations = [
        migrations.RunPython(deepen_sql_content, noop),
    ]
