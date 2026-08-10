from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Next.js",
        "slug": "introduction",
        "order": 1,
        "summary": "A React framework that adds routing, server rendering, and more.",
        "body": """
<p>React itself is just a UI library &mdash; it doesn't decide how pages are routed, how a
project is structured, or how a page gets its data before it's shown. Next.js is a framework
built on top of React that answers those questions, adding file-based routing, built-in
server rendering, and API routes, so you spend less time wiring up infrastructure.</p>
""",
        "example_code": "npx create-next-app@latest my-app\ncd my-app\nnpm run dev",
        "expected_output": "Starts a dev server, usually at http://localhost:3000.",
    },
    {
        "title": "Pages & File-based Routing",
        "slug": "pages-and-routing",
        "order": 2,
        "summary": "A file's location in the app folder decides its URL.",
        "body": """
<p>In Next.js's App Router, a folder under <code>app/</code> containing a
<code>page.js</code> file becomes a route &mdash; no separate routing config to maintain.
<code>app/page.js</code> is the homepage; <code>app/about/page.js</code> becomes
<code>/about</code>.</p>
""",
        "example_code": """// app/about/page.js
export default function AboutPage() {
  return <h1>About us</h1>;
}""",
        "expected_output": "Visiting /about renders an <h1> reading \"About us\".",
    },
    {
        "title": "Server Components vs. Client Components",
        "slug": "server-and-client-components",
        "order": 3,
        "summary": "Deciding what renders on the server vs. what runs in the browser.",
        "body": """
<p>By default, every component in the App Router is a <strong>Server Component</strong>
&mdash; it renders on the server and ships plain HTML to the browser, with no extra
JavaScript for that component. Add <code>"use client"</code> at the top of a file to opt
into a <strong>Client Component</strong> instead, for anything that needs interactivity
(state, event handlers, browser-only APIs).</p>
""",
        "example_code": """"use client";
import { useState } from "react";

export default function LikeButton() {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>{liked ? "Liked!" : "Like"}</button>;
}""",
        "expected_output": "Renders a button reading \"Like\"; clicking it toggles the text to \"Liked!\" and back.",
    },
    {
        "title": "Data Fetching",
        "slug": "data-fetching",
        "order": 4,
        "summary": "Loading data directly inside a Server Component with async/await.",
        "body": """
<p>Server Components can be <code>async</code> functions &mdash; you can
<code>await</code> a database call or an API request directly inside the component, with
no separate data-fetching hook needed, since the code never runs in the browser at all.</p>
""",
        "example_code": """export default async function PostsPage() {
  const res = await fetch("https://api.example.com/posts");
  const posts = await res.json();

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}""",
        "expected_output": "Renders a bulleted list of post titles, fetched fresh on the server before the page is sent to the browser.",
    },
    {
        "title": "API Routes",
        "slug": "api-routes",
        "order": 5,
        "summary": "Writing a backend endpoint inside the same Next.js project.",
        "body": """
<p>A <code>route.js</code> file under <code>app/api/...</code> becomes a backend endpoint
&mdash; export a function named after the HTTP method it should handle
(<code>GET</code>, <code>POST</code>, ...), and return a <code>Response</code>. This lets a
small project keep frontend and backend in one codebase.</p>
""",
        "example_code": """// app/api/hello/route.js
export async function GET() {
  return Response.json({ message: "Hello from the API!" });
}""",
        "expected_output": "A GET request to /api/hello returns: {\"message\": \"Hello from the API!\"}",
    },
    {
        "title": "Linking Between Pages",
        "slug": "linking-between-pages",
        "order": 6,
        "summary": "Client-side navigation with the Link component.",
        "body": """
<p>Use Next.js's <code>&lt;Link&gt;</code> component instead of a plain <code>&lt;a&gt;</code>
tag to navigate between pages &mdash; it pre-fetches the destination page in the background
and swaps content without a full page reload, making navigation feel instant.</p>
""",
        "example_code": """import Link from "next/link";

export default function Nav() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
    </nav>
  );
}""",
        "expected_output": "Renders two navigation links; clicking either updates the page instantly without a full browser reload.",
    },
]


def seed_nextjs_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    frontend = Category.objects.get(slug="frontend")

    subject, _ = Subject.objects.update_or_create(
        slug="nextjs",
        defaults={
            "category": frontend,
            "name": "Next.js",
            "icon": "▲",
            "description": "A React framework that adds file-based routing, server rendering, and API routes.",
            "editor_language": "nextjs",
            "order": 5,
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


def unseed_nextjs_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="nextjs").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0019_seed_react_subject"),
    ]

    operations = [
        migrations.RunPython(seed_nextjs_subject, unseed_nextjs_subject),
    ]
