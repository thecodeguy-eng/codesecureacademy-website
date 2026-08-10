from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A PHP framework that adds structure, routing, and an ORM on top of plain PHP — the same kind of structure Django gives Python.",
        "body": """
<p>Laravel is a PHP framework — it gives raw PHP the same kind of
structure Django gives Python or Express gives JavaScript: routing, an
ORM (Eloquent), templating (Blade), and more, all working together
instead of being hand-built from scratch for every project.</p>

<h2>Example: starting a new project</h2>
<pre><code>composer create-project laravel/laravel my-app
cd my-app
php artisan serve</code></pre>
<pre><code>Starting Laravel development server: http://127.0.0.1:8000</code></pre>
<p><code>artisan</code> is Laravel's command-line tool — you'll use it
constantly for everything from starting a dev server to generating new
files, similar in spirit to Django's <code>manage.py</code>.</p>
""",
    },
    {
        "slug": "routes",
        "summary": "Mapping a URL to the code that should handle it — the simplest routes need no separate controller at all.",
        "body": """
<p>Routes live in <code>routes/web.php</code>. Each one maps a URL
pattern to a closure or a controller method.</p>

<h2>Example: the simplest possible route</h2>
<pre><code>// routes/web.php
Route::get('/', function () {
    return 'Hello, world!';
});</code></pre>
<pre><code>Hello, world!</code></pre>
<p>A route wrapping its logic directly in a closure like this is fine for
something this small — but as logic grows past a line or two, it moves
into a dedicated <strong>controller</strong>, covered next, so
<code>routes/web.php</code> stays readable as a map of "what goes where"
rather than growing into a file full of actual business logic.</p>
""",
    },
    {
        "slug": "controllers",
        "summary": "Grouping related request-handling logic into a class instead of scattering closures across your routes file.",
        "body": """
<p>A controller groups related route logic into one class instead of
scattering closures across <code>routes/web.php</code>.</p>

<h2>Example: a controller and the route pointing at it</h2>
<pre><code>// app/Http/Controllers/PostController.php
class PostController extends Controller
{
    public function index()
    {
        return view('posts.index', ['posts' => Post::all()]);
    }
}

// routes/web.php
Route::get('/posts', [PostController::class, 'index']);</code></pre>
<p>Visiting <code>/posts</code> now runs the controller's
<code>index</code> method, which renders the <code>posts.index</code>
Blade view with every <code>Post</code> passed in as <code>$posts</code>.
Generate one with <code>php artisan make:controller PostController</code>
rather than creating the file by hand — artisan scaffolds the correct
class structure automatically.</p>
""",
    },
    {
        "slug": "eloquent-models",
        "summary": "Laravel's ORM — querying the database using PHP method calls, not raw SQL strings.",
        "body": """
<p>Eloquent is Laravel's ORM: each model class maps to a database table,
and Eloquent infers the table name and columns by convention rather than
requiring you to spell them out manually.</p>

<h2>Example: defining and querying a model</h2>
<pre><code>// app/Models/Post.php
class Post extends Model
{
    protected $fillable = ['title', 'body'];
}

// Usage:
$latest = Post::orderBy('created_at', 'desc')->first();
echo $latest->title;</code></pre>
<p><code>Post::orderBy(...)->first()</code> reads almost like a
sentence, and returns a real PHP object — no SQL string required anywhere
in this code. <code>$fillable</code> is a safety list: only the fields
named there can be mass-assigned from user input at once, which prevents
a visitor from sneaking extra fields (like an <code>is_admin</code> flag)
into a form submission that ends up saved to the database unexpectedly.</p>
""",
    },
    {
        "slug": "blade-templates",
        "summary": "Laravel's templating engine — HTML mixed with {{ }} output and @directives for logic.",
        "body": """
<p>Blade templates (<code>.blade.php</code> files) mix HTML with
<code>{{ $variable }}</code> to print a value (automatically escaped for
safety) and <code>@directives</code> like <code>@foreach</code> and
<code>@if</code> for logic.</p>

<h2>Example: looping over posts in a template</h2>
<pre><code>{{-- resources/views/posts/index.blade.php --}}
&lt;h1&gt;Posts&lt;/h1&gt;
&lt;ul&gt;
  @foreach ($posts as $post)
    &lt;li&gt;{{ $post->title }}&lt;/li&gt;
  @endforeach
&lt;/ul&gt;</code></pre>
<p>Every <code>@foreach</code> needs a matching <code>@endforeach</code>
— Blade directives always come in explicit start/end pairs rather than
relying on indentation, which makes a template's structure unambiguous
even in a long file. <code>{{ }}</code> escaping automatically happens by
default specifically to prevent XSS — a value containing HTML/script tags
gets displayed as harmless plain text instead of being executed, which is
exactly the safe default you want for anything that ultimately came from
user input.</p>
""",
    },
    {
        "slug": "migrations",
        "summary": "Version-controlled changes to your database schema, written in PHP instead of raw SQL.",
        "body": """
<p>A migration is a PHP class describing one change to your database
schema — creating a table, adding a column.</p>

<h2>Example: a migration that creates a table</h2>
<pre><code>// database/migrations/..._create_posts_table.php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('body');
        $table->timestamps();
    });
}</code></pre>
<pre><code>php artisan migrate
</code></pre>
<p>Running <code>php artisan migrate</code> applies every migration that
hasn't run yet, in order, creating a <code>posts</code> table with
<code>id</code>, <code>title</code>, <code>body</code>,
<code>created_at</code>, and <code>updated_at</code> columns
(<code>$table->timestamps()</code> adds the last two automatically). The
real value here: your whole team's database structure stays in sync
through version control — every migration file committed to the repo —
instead of someone manually running ad hoc SQL that only they remember
they ran.</p>
""",
    },
]


def deepen_laravel_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="laravel")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0034_deepen_php_content"),
    ]

    operations = [
        migrations.RunPython(deepen_laravel_content, noop),
    ]
