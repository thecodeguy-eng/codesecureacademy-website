from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Flask",
        "slug": "introduction",
        "order": 1,
        "summary": "A lightweight Python web framework you build up piece by piece.",
        "body": """
<p>Flask is a "micro" Python web framework &mdash; unlike Django, it doesn't ship an ORM or
admin site by default. It gives you routing and request handling, and you add whatever else
you need (a database layer, forms, ...) as separate packages. That makes it a popular choice
for small APIs and services where you want more control over what's included.</p>
""",
        "example_code": """from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Routes & View Functions",
        "slug": "routes-and-views",
        "order": 2,
        "summary": "The @app.route decorator maps a URL to a Python function.",
        "body": """
<p><code>@app.route(path)</code> above a function turns it into a <strong>view</strong>
&mdash; whatever it returns becomes the response body. Add <code>&lt;name&gt;</code> inside
the path to capture part of the URL as a function argument.</p>
""",
        "example_code": """@app.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"
""",
        "expected_output": "Visiting /greet/Ada returns: Hello, Ada!",
    },
    {
        "title": "Templates with Jinja2",
        "slug": "templates",
        "order": 3,
        "summary": "Rendering HTML files with placeholders, Flask's built-in templating engine.",
        "body": """
<p><code>render_template()</code> renders an HTML file from the <code>templates/</code>
folder using Jinja2 &mdash; the same <code>{{ variable }}</code> and
<code>{% for %}</code>/<code>{% if %}</code> tag style Django templates use, since Jinja2
was directly inspired by Django's template language.</p>
""",
        "example_code": """from flask import render_template

@app.route("/posts")
def posts():
    posts = ["First post", "Second post"]
    return render_template("posts.html", posts=posts)

# templates/posts.html
# <ul>
# {% for post in posts %}
#   <li>{{ post }}</li>
# {% endfor %}
# </ul>""",
        "expected_output": "Renders a bulleted list containing \"First post\" and \"Second post\".",
    },
    {
        "title": "Handling Forms",
        "slug": "handling-forms",
        "order": 4,
        "summary": "Reading submitted form data from the request object.",
        "body": """
<p>The global <code>request</code> object carries the incoming request's data.
<code>request.form</code> holds submitted form fields; check
<code>request.method == "POST"</code> before reading them, since a route can accept both GET
and POST by listing both in <code>methods</code>.</p>
""",
        "example_code": """from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return f"Welcome, {username}!"
    return "Please log in."
""",
        "expected_output": "A GET request returns \"Please log in.\"; a POST with username=Ada returns \"Welcome, Ada!\"",
    },
    {
        "title": "Flask-SQLAlchemy Models",
        "slug": "flask-sqlalchemy",
        "order": 5,
        "summary": "Adding an ORM to Flask with the SQLAlchemy extension.",
        "body": """
<p>Flask doesn't include an ORM out of the box, so most projects add
<strong>Flask-SQLAlchemy</strong>. Define a model as a class with typed columns, then query
it with familiar-looking methods like <code>.query.all()</code>.</p>
""",
        "example_code": """from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

# Usage:
posts = Post.query.all()""",
        "expected_output": "posts becomes a Python list of every Post row in the database.",
    },
    {
        "title": "Blueprints",
        "slug": "blueprints",
        "order": 6,
        "summary": "Splitting a large Flask app into smaller, reusable pieces.",
        "body": """
<p>As a Flask app grows, a <strong>Blueprint</strong> lets you group related routes into
their own file/module, then register it on the main app &mdash; similar in spirit to how a
Django project splits into multiple apps.</p>
""",
        "example_code": """# blog/routes.py
from flask import Blueprint

blog = Blueprint("blog", __name__)

@blog.route("/blog")
def blog_home():
    return "Welcome to the blog"

# app.py
from blog.routes import blog
app.register_blueprint(blog)""",
        "expected_output": "Visiting /blog now returns: Welcome to the blog",
    },
]


def seed_flask_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    backend = Category.objects.get(slug="backend")

    subject, _ = Subject.objects.update_or_create(
        slug="flask",
        defaults={
            "category": backend,
            "name": "Flask",
            "icon": "\U0001F9EA",
            "description": "A lightweight Python web framework you build up piece by piece.",
            "editor_language": "flask",
            "order": 7,
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


def unseed_flask_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="flask").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0021_seed_laravel_subject"),
    ]

    operations = [
        migrations.RunPython(seed_flask_subject, unseed_flask_subject),
    ]
