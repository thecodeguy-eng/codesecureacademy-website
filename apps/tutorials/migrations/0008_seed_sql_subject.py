from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to SQL",
        "slug": "introduction",
        "order": 1,
        "summary": "How SQL talks to a database made of tables, rows, and columns.",
        "body": """
<p>SQL (Structured Query Language) is how you read and write data stored in a relational
database. Data lives in <strong>tables</strong> &mdash; think of a table like a spreadsheet,
with named <strong>columns</strong> and one <strong>row</strong> per record. Every example
below queries a <code>students</code> table with columns <code>id</code>, <code>name</code>,
<code>track</code>, and <code>score</code>.</p>
""",
        "example_code": "SELECT * FROM students;",
        "expected_output": "id | name  | track         | score\n1  | Ada   | Frontend      | 92\n2  | Chidi | Cybersecurity | 78\n3  | Musa  | Backend       | 85",
    },
    {
        "title": "SELECT",
        "slug": "select",
        "order": 2,
        "summary": "Choosing which columns to retrieve.",
        "body": """
<p><code>SELECT</code> picks which columns you want back. <code>*</code> means "every
column"; naming specific columns (comma-separated) returns just those.</p>
""",
        "example_code": "SELECT name, score FROM students;",
        "expected_output": "name  | score\nAda   | 92\nChidi | 78\nMusa  | 85",
    },
    {
        "title": "WHERE",
        "slug": "where",
        "order": 3,
        "summary": "Filtering rows with a condition.",
        "body": """
<p><code>WHERE</code> filters which rows come back, based on a condition. Combine
conditions with <code>AND</code> / <code>OR</code>, same as most languages' logical operators.</p>
""",
        "example_code": "SELECT name, score FROM students WHERE score >= 85;",
        "expected_output": "name | score\nAda  | 92\nMusa | 85",
    },
    {
        "title": "ORDER BY",
        "slug": "order-by",
        "order": 4,
        "summary": "Sorting results ascending or descending.",
        "body": """
<p><code>ORDER BY column</code> sorts the results. Add <code>DESC</code> for
descending order (highest/latest first) &mdash; the default without it is ascending.</p>
""",
        "example_code": "SELECT name, score FROM students ORDER BY score DESC;",
        "expected_output": "name  | score\nAda   | 92\nMusa  | 85\nChidi | 78",
    },
    {
        "title": "INSERT INTO",
        "slug": "insert-into",
        "order": 5,
        "summary": "Adding a new row to a table.",
        "body": """
<p><code>INSERT INTO table (columns) VALUES (values)</code> adds a new row. List the
columns you're filling in, then the matching values in the same order.</p>
""",
        "example_code": "INSERT INTO students (name, track, score)\nVALUES ('Ngozi', 'Frontend', 88);",
        "expected_output": "1 row inserted.",
    },
    {
        "title": "UPDATE & DELETE",
        "slug": "update-and-delete",
        "order": 6,
        "summary": "Changing existing rows, and removing them.",
        "body": """
<p><code>UPDATE table SET column = value WHERE condition</code> changes existing rows
&mdash; the <code>WHERE</code> clause is important, since leaving it off updates
<em>every</em> row. <code>DELETE FROM table WHERE condition</code> removes rows the same
way.</p>
""",
        "example_code": "UPDATE students SET score = 95 WHERE name = 'Chidi';",
        "expected_output": "1 row updated.",
    },
    {
        "title": "JOIN",
        "slug": "join",
        "order": 7,
        "summary": "Combining rows from two related tables.",
        "body": """
<p>Real databases split data across multiple tables that reference each other. A
<code>JOIN</code> combines rows from two tables based on a matching column &mdash;
here, matching each student's <code>track</code> to a row in a separate
<code>tracks</code> table that stores each track's cohort start date.</p>
""",
        "example_code": "SELECT students.name, tracks.start_date\nFROM students\nJOIN tracks ON students.track = tracks.name;",
        "expected_output": "name  | start_date\nAda   | 2026-09-01\nChidi | 2026-10-15\nMusa  | 2026-09-01",
    },
    {
        "title": "Aggregate Functions",
        "slug": "aggregate-functions",
        "order": 8,
        "summary": "COUNT, SUM, AVG, MIN, and MAX — summarizing many rows into one value.",
        "body": """
<p>Aggregate functions compute a single value across many rows: <code>COUNT()</code> counts
rows, <code>SUM()</code> totals a column, <code>AVG()</code> averages it,
<code>MIN()</code>/<code>MAX()</code> find the smallest/largest value. Combine with
<code>GROUP BY</code> to get one result per group instead of one for the whole table.</p>
""",
        "example_code": "SELECT track, AVG(score) AS avg_score\nFROM students\nGROUP BY track;",
        "expected_output": "track         | avg_score\nFrontend      | 90.0\nCybersecurity | 78.0\nBackend       | 85.0",
    },
]


def seed_sql_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="sql",
        defaults={
            "name": "SQL",
            "icon": "\U0001F5C4️",
            "description": "The language for querying and managing data in a relational database.",
            "editor_language": "sql",
            "order": 6,
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
                "expected_output": data["expected_output"],
            },
        )


def unseed_sql_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="sql").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0007_seed_php_subject"),
    ]

    operations = [
        migrations.RunPython(seed_sql_subject, unseed_sql_subject),
    ]
