from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A lightweight Python web framework you build up piece by piece — what 'micro-framework' actually means in practice.",
        "body": """
<p>Flask is a "micro" Python web framework — unlike Django, it doesn't
ship an ORM or admin site by default. It gives you routing and request
handling, and you add whatever else you need (a database layer, forms)
as separate packages, chosen deliberately rather than bundled in.</p>

<h2>Example: the smallest complete Flask app</h2>
<pre><code>from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)</code></pre>
<pre><code>Hello, world!</code></pre>
<p>That's a genuinely complete, runnable web application in nine lines —
Flask's minimalism is exactly why it's a popular choice for small APIs
and services where you want fine control over what's included, rather
than Django's more complete, more opinionated "batteries included"
approach.</p>
""",
    },
    {
        "slug": "routes-and-views",
        "summary": "The @app.route decorator maps a URL to a Python function, and how to capture part of the URL as an argument.",
        "body": """
<p><code>@app.route(path)</code> above a function turns it into a
<strong>view</strong> — whatever it returns becomes the response body.</p>

<h2>Example: capturing part of the URL</h2>
<pre><code>@app.route("/greet/<name>")
def greet(name):
    return f"Hello, {name}!"</code></pre>
<pre><code>Visiting /greet/Ada returns: Hello, Ada!</code></pre>
<p><code>&lt;name&gt;</code> inside the path captures that segment of the
URL and passes it straight into the function as an argument named
<code>name</code> — the same underlying idea as Next.js's
<code>[slug]</code> dynamic routes or Laravel's route parameters, just
Flask's specific syntax for it.</p>
""",
    },
    {
        "slug": "templates",
        "summary": "Rendering HTML files with placeholders using Jinja2, Flask's built-in templating engine.",
        "body": """
<p><code>render_template()</code> renders an HTML file from the
<code>templates/</code> folder using Jinja2.</p>

<h2>Example: rendering a list of posts</h2>
<pre><code>from flask import render_template

@app.route("/posts")
def posts():
    posts = ["First post", "Second post"]
    return render_template("posts.html", posts=posts)

# templates/posts.html:
# &lt;ul&gt;
# {% for post in posts %}
#   &lt;li&gt;{{ post }}&lt;/li&gt;
# {% endfor %}
# &lt;/ul&gt;</code></pre>
<pre><code>Renders a bulleted list: First post, Second post</code></pre>
<p>Jinja2 uses the same <code>{{ variable }}</code> and
<code>{% for %}</code>/<code>{% if %}</code> tag style Django templates
use — no coincidence, since Jinja2 was directly inspired by Django's
template language. If you've read the Django tutorial's Templates lesson,
this syntax should already feel familiar.</p>
""",
    },
    {
        "slug": "handling-forms",
        "summary": "Reading submitted form data from the request object, and the method check that decides how to respond.",
        "body": """
<p>The global <code>request</code> object carries the incoming request's
data. <code>request.form</code> holds submitted form fields.</p>

<h2>Example: a login route handling both GET and POST</h2>
<pre><code>from flask import request

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        return f"Welcome, {username}!"
    return "Please log in."</code></pre>
<pre><code>GET  /login          -> "Please log in."
POST /login (username=Ada) -> "Welcome, Ada!"</code></pre>
<p>By default a route only accepts <code>GET</code> — listing both
<code>"GET"</code> and <code>"POST"</code> in <code>methods</code> lets
one single view handle showing the empty form (GET, when a visitor first
arrives) and processing the submitted data (POST, after they submit it),
branching on <code>request.method</code> to tell the two cases apart.</p>
""",
    },
    {
        "slug": "flask-sqlalchemy",
        "summary": "Adding an ORM to Flask with the SQLAlchemy extension, since Flask doesn't include one by default.",
        "body": """
<p>Flask doesn't include an ORM out of the box, so most real projects add
<strong>Flask-SQLAlchemy</strong> — a deliberate choice, not a missing
feature, in keeping with Flask's "add only what you need" philosophy.</p>

<h2>Example: a model and a query</h2>
<pre><code>from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))

# Usage:
posts = Post.query.all()</code></pre>
<p><code>Post.query.all()</code> returns a Python list of every
<code>Post</code> row — familiar-looking if you've seen Django's
<code>Post.objects.all()</code> or Laravel's <code>Post::all()</code>,
since all three frameworks solve the same underlying problem (querying a
database without writing raw SQL) with genuinely similar-shaped APIs.</p>
""",
    },
    {
        "slug": "blueprints",
        "summary": "Splitting a large Flask app into smaller, reusable pieces — Flask's answer to Django's multi-app structure.",
        "body": """
<p>As a Flask app grows past a handful of routes, a
<strong>Blueprint</strong> lets you group related routes into their own
file or module, then register it on the main app.</p>

<h2>Example: a blueprint for a blog section</h2>
<pre><code># blog/routes.py
from flask import Blueprint

blog = Blueprint("blog", __name__)

@blog.route("/blog")
def blog_home():
    return "Welcome to the blog"

# app.py
from blog.routes import blog
app.register_blueprint(blog)</code></pre>
<pre><code>Visiting /blog now returns: Welcome to the blog</code></pre>
<p>This is Flask's version of splitting a project into pieces, similar in
spirit to how a Django project splits into multiple apps (like this
platform's own <code>tutorials</code> and <code>courses</code> apps) —
each blueprint owns its own routes, keeping one giant
<code>app.py</code> from becoming unmanageable as a real project grows.</p>
""",
    },
]


def deepen_flask_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="flask")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0035_deepen_laravel_content"),
    ]

    operations = [
        migrations.RunPython(deepen_flask_content, noop),
    ]
