from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A Python web framework for building sites fast, with batteries included — what 'batteries included' actually means in practice.",
        "body": """
<p>Django is a Python framework for building web applications — it comes
with an ORM (database layer), an admin interface, a templating engine,
and routing all built in, so you spend less time wiring things together
and choosing between competing packages before you can even start. This
entire site is a Django project, built with everything covered in this
subject.</p>

<h2>Example: starting a brand new project</h2>
<pre><code>django-admin startproject myproject
cd myproject
python manage.py runserver</code></pre>
<pre><code>Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.</code></pre>
<p>Compare this to Flask's deliberately minimal starting point in the
Flask subject — Django takes the opposite philosophy on purpose: give you
a complete, opinionated structure from the very first command, so a team
doesn't have to independently decide how to organize routing, templates,
and database access on every new project.</p>
""",
    },
    {
        "slug": "project-and-app-structure",
        "summary": "A Django project is made of one or more apps, each a self-contained feature — the same structure this actual platform uses.",
        "body": """
<p>A Django <strong>project</strong> is the whole site's configuration
(settings, root URLs). Inside it, you create one or more
<strong>apps</strong> — each a self-contained piece of functionality.</p>

<h2>Example: scaffolding a new app</h2>
<pre><code>python manage.py startapp blog</code></pre>
<pre><code>Creates a blog/ folder containing models.py, views.py, admin.py,
migrations/, and more.</code></pre>
<p>This isn't just a tutorial convention — it's exactly how real Django
projects, including this platform, are organized: separate apps for
distinct concerns (this site has one for lessons, one for paid courses,
one for the marketplace, one for payments), each with its own models,
views, and admin registration, all plugged into one shared project.
Splitting by app keeps each piece independently understandable, instead
of one enormous file holding everything.</p>
""",
    },
    {
        "slug": "models",
        "summary": "Defining your database tables as Python classes — and the two-command cycle every model change goes through.",
        "body": """
<p>A Django <strong>model</strong> is a Python class describing one
database table — each class attribute becomes a column.</p>

<h2>Example: a Post model</h2>
<pre><code># blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title</code></pre>
<pre><code>python manage.py makemigrations
python manage.py migrate</code></pre>
<p>After changing a model, <code>makemigrations</code> generates a file
describing exactly what changed, and <code>migrate</code> actually
applies it to the database — creating a <code>blog_post</code> table with
<code>title</code>, <code>body</code>, and <code>published_at</code>
columns. This two-step cycle (generate, then apply) is deliberate: the
generated migration file is itself real, reviewable, version-controlled
code, so your whole team's database structure stays in sync through git,
not through someone remembering to run a manual SQL command.</p>
""",
    },
    {
        "slug": "views",
        "summary": "Python functions that take a request and return a response — where you fetch data and decide what to send back.",
        "body": """
<p>A <strong>view</strong> is a Python function (or class) that receives
an incoming <code>request</code> and returns a <code>response</code>.</p>

<h2>Example: a view listing posts, newest first</h2>
<pre><code># blog/views.py
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})</code></pre>
<pre><code>Renders the blog/post_list.html template with every Post, newest
first, available as {{ posts }}.</code></pre>
<p><code>Post.objects.all().order_by('-published_at')</code> is Django's
ORM — the same kind of query you saw in the SQL tutorial's ORDER BY
lesson, expressed as Python method calls instead of a raw SQL string. The
leading <code>-</code> before <code>published_at</code> means descending
order, exactly matching SQL's <code>ORDER BY published_at DESC</code>.
<code>render()</code> is the bridge between a view's Python data and the
actual HTML template that displays it — covered properly two lessons
from now.</p>
""",
    },
    {
        "slug": "urls-and-routing",
        "summary": "Mapping a URL path to the view that should handle it — and how a project stitches every app's URLs together.",
        "body": """
<p>Each app defines its own <code>urls.py</code> mapping a path pattern
to a view. The project's root <code>urls.py</code> then
<code>include()</code>s each app's URLs under a prefix.</p>

<h2>Example: one app's URLs, included into the project</h2>
<pre><code># blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
]

# myproject/urls.py
from django.urls import include, path
urlpatterns = [
    path('blog/', include('blog.urls')),
]</code></pre>
<pre><code>Requests to /blog/ are routed to the post_list view.</code></pre>
<p>This is exactly how this actual platform's own URLs are structured —
each app owns its own <code>urls.py</code> (tutorials, courses,
marketplace, each independently), and the root <code>urls.py</code>
mounts every one of them under its own prefix. <code>app_name</code>
matters for a real practical reason: it lets templates reference
<code>{% url 'blog:post_list' %}</code> unambiguously, even if a
different app also happens to have a view named <code>post_list</code>.</p>
""",
    },
    {
        "slug": "templates",
        "summary": "HTML files with placeholders Django fills in with real data — {{ }} vs {% %}, and why the distinction matters.",
        "body": """
<p>A Django <strong>template</strong> is an HTML file with special tags:
<code>{{ variable }}</code> prints a value, and <code>{% tag %}</code>
handles logic like loops and conditionals.</p>

<h2>Example: looping and handling the empty case</h2>
<pre><code>{# blog/post_list.html #}
&lt;h1&gt;Blog Posts&lt;/h1&gt;
&lt;ul&gt;
  {% for post in posts %}
    &lt;li&gt;{{ post.title }}&lt;/li&gt;
  {% empty %}
    &lt;li&gt;No posts yet.&lt;/li&gt;
  {% endfor %}
&lt;/ul&gt;</code></pre>
<pre><code>Renders a bulleted list of every post's title, or "No posts yet."
if the posts list is empty.</code></pre>
<p>The view's context dictionary (that <code>{'posts': posts}</code> from
the Views lesson) is exactly what fills these placeholders in —
<code>{{ post.title }}</code> reads the <code>title</code> attribute off
each <code>Post</code> object the view passed in. <code>{% empty %}</code>
is a small but genuinely useful detail — it renders only when the loop
had nothing to iterate over at all, sparing you from writing a separate
<code>{% if %}</code> just to handle an empty list gracefully.</p>
""",
    },
    {
        "slug": "admin-site",
        "summary": "A free, auto-generated interface for managing your data — how this platform's own admin approval workflows are actually built.",
        "body": """
<p>Registering a model with Django's admin gives you a working
create/read/update/delete interface at <code>/admin/</code>, with zero
extra HTML to write.</p>

<h2>Example: registering a model with the admin</h2>
<pre><code># blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')</code></pre>
<pre><code>Visiting /admin/ now shows a "Posts" section listing every post's
title and publish date, editable in the browser.</code></pre>
<p>This is exactly the mechanism behind every "an admin approves this"
workflow on a real platform — a course going live only after review, a
tutor's application being approved, all handled through
<code>ModelAdmin</code> classes just like this one, sometimes with custom
<strong>admin actions</strong> (a button that runs a specific bit of
Python against selected rows) added on top for things like "approve
selected." The admin site is meant for trusted staff, not public-facing
use — it isn't a substitute for the actual public pages your visitors see.</p>
""",
    },
    {
        "slug": "forms",
        "summary": "Validating user input and saving it, with far less boilerplate than raw HTML forms — and why you still check request.method.",
        "body": """
<p>A <code>ModelForm</code> generates form fields (and validation)
straight from a model, so you don't hand-write and re-validate every
input separately.</p>

<h2>Example: a form generated from a model, and the view that uses it</h2>
<pre><code># blog/forms.py
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

# blog/views.py
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form})</code></pre>
<pre><code>A GET request shows an empty form; a valid POST creates a new Post
row and re-shows the (now empty) form.</code></pre>
<p>The <code>request.method == 'POST'</code> check is doing real work
here — it's exactly what the Backend track's requests-and-responses
lesson and the Flask tutorial's forms lesson both cover: one single view
handling both "show the empty form" (GET) and "process the submitted
data" (POST), branching on the method. <code>form.is_valid()</code>
re-validates on the server regardless of anything the browser already
checked — the same server-side validation principle the HTML tutorial's
Forms lesson introduced, here handled almost entirely by Django rather
than code you'd write by hand.</p>
""",
    },
]


def deepen_django_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="django")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0042_deepen_flutter_content"),
    ]

    operations = [
        migrations.RunPython(deepen_django_content, noop),
    ]
