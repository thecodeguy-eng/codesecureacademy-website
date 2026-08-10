from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A React framework that adds routing, server rendering, and more — what it adds on top of React that React alone doesn't decide for you.",
        "body": """
<p>React itself is just a UI library — it doesn't decide how pages are
routed, how a project is structured, or how a page gets its data before
it's shown to a visitor. Next.js is a framework built on top of React
that answers those exact questions, so a team doesn't have to invent its
own answer to each one from scratch.</p>

<h2>Example: starting a new project</h2>
<pre><code>npx create-next-app@latest my-app
cd my-app
npm run dev</code></pre>
<p>This scaffolds a working project with routing, a build system, and
sensible defaults already wired up, then starts a local dev server — the
kind of setup that would otherwise take real, careful configuration to
assemble by hand from plain React alone.</p>
""",
    },
    {
        "slug": "pages-and-routing",
        "summary": "A file's location in the app folder decides its URL — no separate routing configuration file to maintain.",
        "body": """
<p>In Next.js's App Router, a folder under <code>app/</code> containing a
<code>page.js</code> file automatically becomes a route.</p>

<h2>Example: two routes from two files</h2>
<pre><code>app/page.js           -> the homepage,        "/"
app/about/page.js      -> becomes             "/about"
app/blog/[slug]/page.js -> becomes            "/blog/anything-here"</code></pre>
<pre><code>// app/about/page.js
export default function AboutPage() {
  return &lt;h1&gt;About us&lt;/h1&gt;;
}</code></pre>
<p>Notice the third example: square brackets in a folder name
(<code>[slug]</code>) create a <strong>dynamic route</strong> — one file
that handles <em>any</em> value in that position of the URL, with the
actual value (<code>"anything-here"</code>) available inside the
component as a parameter. This is exactly how a blog with hundreds of
posts is served from one single page file instead of one file per post.</p>
""",
    },
    {
        "slug": "server-and-client-components",
        "summary": "Deciding what renders on the server vs. what runs in the browser — and the one line that changes it.",
        "body": """
<p>By default, every component in the App Router is a <strong>Server
Component</strong> — it renders on the server and ships plain HTML to
the browser, with no extra JavaScript sent down for that component at
all.</p>

<h2>Example: opting into interactivity</h2>
<pre><code>"use client";
import { useState } from "react";

export default function LikeButton() {
  const [liked, setLiked] = useState(false);
  return &lt;button onClick={() => setLiked(!liked)}&gt;{liked ? "Liked!" : "Like"}&lt;/button&gt;;
}</code></pre>
<p>Add <code>"use client"</code> at the very top of a file to opt into a
<strong>Client Component</strong> instead, for anything that needs real
browser interactivity — state, event handlers, browser-only APIs like
<code>localStorage</code>. React's <code>useState</code> and
<code>useEffect</code> only work in Client Components; a plain Server
Component can't use them at all, since they depend on code actually
running in the browser.</p>

<h2>Why this split is worth the extra decision</h2>
<p>Every component you <em>don't</em> mark as a Client Component ships
zero extra JavaScript to the visitor's browser — real performance benefit
at scale, especially on slower connections and devices. The practical
rule of thumb: default to a Server Component, and only add
<code>"use client"</code> to the specific, usually small components that
genuinely need interactivity — not the whole page just because one button
on it needs a click handler.</p>
""",
    },
    {
        "slug": "data-fetching",
        "summary": "Loading data directly inside a Server Component with async/await — no separate data-fetching hook required.",
        "body": """
<p>Server Components can be <code>async</code> functions — you can
<code>await</code> a database call or an API request directly inside the
component.</p>

<h2>Example: fetching and rendering a list</h2>
<pre><code>export default async function PostsPage() {
  const res = await fetch("https://api.example.com/posts");
  const posts = await res.json();

  return (
    &lt;ul&gt;
      {posts.map((post) => (
        &lt;li key={post.id}&gt;{post.title}&lt;/li&gt;
      ))}
    &lt;/ul&gt;
  );
}</code></pre>
<p>Because this component runs on the server, not in the browser, the
<code>fetch</code> call — and the credentials or private URLs it might
need — never has to be exposed to the client at all. Compare this to
plain React, where you'd typically need a separate <code>useEffect</code>
plus <code>useState</code> just to load the same data after the
component first renders; here, the data is already resolved by the time
the HTML reaches the browser at all, which also means there's no
"loading..." flash for this particular content.</p>
""",
    },
    {
        "slug": "api-routes",
        "summary": "Writing a backend endpoint inside the same Next.js project — keeping frontend and backend in one codebase.",
        "body": """
<p>A <code>route.js</code> file under <code>app/api/...</code> becomes a
real backend endpoint.</p>

<h2>Example: a tiny API endpoint</h2>
<pre><code>// app/api/hello/route.js
export async function GET() {
  return Response.json({ message: "Hello from the API!" });
}</code></pre>
<p>Export a function named after the HTTP method it should handle
(<code>GET</code>, <code>POST</code>, and so on — the same methods from
the backend track's requests-and-responses lesson), and return a
<code>Response</code>. A request to <code>/api/hello</code> now returns
real JSON, no separate backend server or separate deployment required —
this small project can keep its frontend and backend together in one
codebase, which is exactly why API routes are popular for small apps and
prototypes.</p>
""",
    },
    {
        "slug": "linking-between-pages",
        "summary": "Client-side navigation with the Link component — why it's faster than a plain anchor tag for internal links.",
        "body": """
<p>Use Next.js's <code>&lt;Link&gt;</code> component instead of a plain
<code>&lt;a&gt;</code> tag to navigate between pages within your own app.</p>

<h2>Example: navigation with Link</h2>
<pre><code>import Link from "next/link";

export default function Nav() {
  return (
    &lt;nav&gt;
      &lt;Link href="/"&gt;Home&lt;/Link&gt;
      &lt;Link href="/about"&gt;About&lt;/Link&gt;
    &lt;/nav&gt;
  );
}</code></pre>
<p>A plain <code>&lt;a href="/about"&gt;</code> would work too — but it
triggers a full page reload, throwing away everything already loaded and
starting fresh. <code>&lt;Link&gt;</code> pre-fetches the destination
page's content in the background as soon as it becomes visible, then
swaps content in without a full reload when clicked, making navigation
between pages of your own app feel close to instant. Reserve a plain
<code>&lt;a&gt;</code> for links leaving your site entirely — for
internal navigation within a Next.js app, <code>&lt;Link&gt;</code> is
almost always the right choice.</p>
""",
    },
]


def deepen_nextjs_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="nextjs")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0031_deepen_react_content"),
    ]

    operations = [
        migrations.RunPython(deepen_nextjs_content, noop),
    ]
