from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Django",
        "slug": "introduction",
        "order": 1,
        "summary": "A Python web framework for building sites fast, with batteries included.",
        "body": """
<p>Django is a Python framework for building web applications &mdash; it comes with an ORM
(database layer), an admin interface, a templating engine, and routing all built in, so you
spend less time wiring things together. This entire site is a Django project. A brand new
project starts with two commands.</p>
""",
        "example_code": """django-admin startproject myproject
cd myproject
python manage.py runserver""",
        "expected_output": "Starting development server at http://127.0.0.1:8000/\nQuit the server with CTRL-BREAK.",
    },
    {
        "title": "Project & App Structure",
        "slug": "project-and-app-structure",
        "order": 2,
        "summary": "A Django project is made of one or more apps, each a self-contained feature.",
        "body": """
<p>A Django <strong>project</strong> is the whole site's configuration (settings, root URLs).
Inside it, you create one or more <strong>apps</strong> &mdash; each a self-contained piece
of functionality (a blog, a store, in this project's case things like <code>tutorials</code>
and <code>courses</code>). <code>startapp</code> scaffolds a new one.</p>
""",
        "example_code": """python manage.py startapp blog""",
        "expected_output": "Creates a blog/ folder containing models.py, views.py, admin.py, migrations/, and more.",
    },
    {
        "title": "Models",
        "slug": "models",
        "order": 3,
        "summary": "Defining your database tables as Python classes.",
        "body": """
<p>A Django <strong>model</strong> is a Python class describing one database table &mdash;
each class attribute becomes a column. Django's ORM lets you query the database with Python
instead of writing raw SQL. After changing a model, run
<code>makemigrations</code> then <code>migrate</code> to apply the change to the database.</p>
""",
        "example_code": """# blog/models.py
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title""",
        "expected_output": "python manage.py makemigrations && python manage.py migrate\ncreates a `blog_post` table with title, body, and published_at columns.",
    },
    {
        "title": "Views",
        "slug": "views",
        "order": 4,
        "summary": "Python functions that take a request and return a response.",
        "body": """
<p>A <strong>view</strong> is a Python function (or class) that receives an incoming
<code>request</code> and returns a <code>response</code> &mdash; usually rendered HTML, but
it could be JSON, a redirect, or anything else. This is where you fetch data with the ORM
and decide what to send back.</p>
""",
        "example_code": """# blog/views.py
from django.shortcuts import render
from .models import Post

def post_list(request):
    posts = Post.objects.all().order_by('-published_at')
    return render(request, 'blog/post_list.html', {'posts': posts})""",
        "expected_output": "Renders the blog/post_list.html template with every Post, newest first, available as {{ posts }}.",
    },
    {
        "title": "URLs & Routing",
        "slug": "urls-and-routing",
        "order": 5,
        "summary": "Mapping a URL path to the view that should handle it.",
        "body": """
<p>Each app defines its own <code>urls.py</code> mapping a path pattern to a view. The
project's root <code>urls.py</code> then <code>include()</code>s each app's URLs under a
prefix &mdash; exactly how this site wires up <code>/tutorials/</code> and
<code>/courses/</code> as separate apps.</p>
""",
        "example_code": """# blog/urls.py
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
]""",
        "expected_output": "Requests to /blog/ are routed to the post_list view.",
    },
    {
        "title": "Templates",
        "slug": "templates",
        "order": 6,
        "summary": "HTML files with placeholders Django fills in with real data.",
        "body": """
<p>A Django <strong>template</strong> is an HTML file with special tags:
<code>{{ variable }}</code> prints a value, and <code>{% tag %}</code> handles logic like
loops (<code>{% for %}</code>) and conditionals (<code>{% if %}</code>). The view's context
dictionary (the third argument to <code>render()</code>) is what fills those placeholders in.</p>
""",
        "example_code": """{# blog/post_list.html #}
<h1>Blog Posts</h1>
<ul>
  {% for post in posts %}
    <li>{{ post.title }}</li>
  {% empty %}
    <li>No posts yet.</li>
  {% endfor %}
</ul>""",
        "expected_output": "Renders a bulleted list of every post's title, or \"No posts yet.\" if the posts list is empty.",
    },
    {
        "title": "The Admin Site",
        "slug": "admin-site",
        "order": 7,
        "summary": "A free, auto-generated interface for managing your data.",
        "body": """
<p>Registering a model with Django's admin gives you a working create/read/update/delete
interface at <code>/admin/</code>, with zero extra HTML to write &mdash; this project's own
admin (where courses and tutors get approved) is exactly this feature. It's meant for
trusted staff, not public-facing use.</p>
""",
        "example_code": """# blog/admin.py
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at')""",
        "expected_output": "Visiting /admin/ now shows a \"Posts\" section listing every post's title and publish date, editable in the browser.",
    },
    {
        "title": "Forms",
        "slug": "forms",
        "order": 8,
        "summary": "Validating user input and saving it, with far less boilerplate than raw HTML forms.",
        "body": """
<p>A <code>ModelForm</code> generates form fields (and validation) straight from a model,
so you don't hand-write and re-validate every input. In the view, check
<code>request.method == 'POST'</code> and call <code>form.is_valid()</code> before saving
&mdash; the same pattern this site's own apply-as-tutor and create-course forms use.</p>
""",
        "example_code": """# blog/forms.py
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
    return render(request, 'blog/new_post.html', {'form': form})""",
        "expected_output": "A GET request shows an empty form; a valid POST creates a new Post row and re-shows the (now empty) form.",
    },
]


def seed_django_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="django",
        defaults={
            "name": "Django",
            "icon": "\U0001F996",
            "description": "A Python web framework for building sites fast, with an ORM, admin, and templating built in.",
            "editor_language": "django",
            "order": 12,
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


def unseed_django_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="django").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0014_seed_flutter_subject"),
    ]

    operations = [
        migrations.RunPython(seed_django_subject, unseed_django_subject),
    ]
