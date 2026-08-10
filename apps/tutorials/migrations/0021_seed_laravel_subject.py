from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Laravel",
        "slug": "introduction",
        "order": 1,
        "summary": "A PHP framework that adds structure, routing, and an ORM on top of plain PHP.",
        "body": """
<p>Laravel is a PHP framework &mdash; it gives raw PHP the same kind of structure Django
gives Python: routing, an ORM (Eloquent), templating (Blade), and more, all working together
instead of being hand-built from scratch. A new project starts with the Laravel installer or
Composer.</p>
""",
        "example_code": "composer create-project laravel/laravel my-app\ncd my-app\nphp artisan serve",
        "expected_output": "Starting Laravel development server: http://127.0.0.1:8000",
    },
    {
        "title": "Routes",
        "slug": "routes",
        "order": 2,
        "summary": "Mapping a URL to the code that should handle it.",
        "body": """
<p>Routes live in <code>routes/web.php</code>. Each one maps a URL pattern to a closure or a
controller method &mdash; the simplest routes can return a response directly without a
separate controller at all.</p>
""",
        "example_code": """// routes/web.php
Route::get('/', function () {
    return 'Hello, world!';
});""",
        "expected_output": "Hello, world!",
    },
    {
        "title": "Controllers",
        "slug": "controllers",
        "order": 3,
        "summary": "Grouping related request-handling logic into a class.",
        "body": """
<p>A controller groups related route logic into one class instead of scattering closures
across <code>routes/web.php</code>. Generate one with <code>php artisan make:controller</code>,
then point a route at one of its methods.</p>
""",
        "example_code": """// app/Http/Controllers/PostController.php
class PostController extends Controller
{
    public function index()
    {
        return view('posts.index', ['posts' => Post::all()]);
    }
}

// routes/web.php
Route::get('/posts', [PostController::class, 'index']);""",
        "expected_output": "Visiting /posts renders the posts.index Blade view with every Post passed in as $posts.",
    },
    {
        "title": "Eloquent Models",
        "slug": "eloquent-models",
        "order": 4,
        "summary": "Laravel's ORM — query the database using PHP, not raw SQL.",
        "body": """
<p>Eloquent is Laravel's ORM: each model class maps to a database table, and Eloquent infers
the table name and columns by convention. <code>Post::all()</code>,
<code>Post::find($id)</code>, and <code>Post::where(...)</code> all return real PHP objects,
no SQL required.</p>
""",
        "example_code": """// app/Models/Post.php
class Post extends Model
{
    protected $fillable = ['title', 'body'];
}

// Usage:
$latest = Post::orderBy('created_at', 'desc')->first();
echo $latest->title;""",
        "expected_output": "Prints the title of the most recently created post.",
    },
    {
        "title": "Blade Templates",
        "slug": "blade-templates",
        "order": 5,
        "summary": "Laravel's templating engine — HTML with {{ }} and @directives.",
        "body": """
<p>Blade templates (<code>.blade.php</code> files) mix HTML with <code>{{ $variable }}</code>
to print a value (auto-escaped for safety) and <code>@directives</code> like
<code>@foreach</code>/<code>@endforeach</code> and <code>@if</code>/<code>@endif</code> for
logic.</p>
""",
        "example_code": """{{-- resources/views/posts/index.blade.php --}}
<h1>Posts</h1>
<ul>
  @foreach ($posts as $post)
    <li>{{ $post->title }}</li>
  @endforeach
</ul>""",
        "expected_output": "Renders a bulleted list of every post's title.",
    },
    {
        "title": "Migrations",
        "slug": "migrations",
        "order": 6,
        "summary": "Version-controlled changes to your database schema, written in PHP.",
        "body": """
<p>A migration is a PHP class describing one change to your database schema &mdash; creating
a table, adding a column. Running <code>php artisan migrate</code> applies every migration
that hasn't run yet, so your whole team's database structure stays in sync via version
control instead of manual SQL.</p>
""",
        "example_code": """// database/migrations/..._create_posts_table.php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('body');
        $table->timestamps();
    });
}""",
        "expected_output": "php artisan migrate\ncreates a `posts` table with id, title, body, created_at, and updated_at columns.",
    },
]


def seed_laravel_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    backend = Category.objects.get(slug="backend")

    subject, _ = Subject.objects.update_or_create(
        slug="laravel",
        defaults={
            "category": backend,
            "name": "Laravel",
            "icon": "\U0001F534",
            "description": "A PHP framework adding routing, an ORM, and templating on top of plain PHP.",
            "editor_language": "laravel",
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


def unseed_laravel_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="laravel").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0020_seed_nextjs_subject"),
    ]

    operations = [
        migrations.RunPython(seed_laravel_subject, unseed_laravel_subject),
    ]
