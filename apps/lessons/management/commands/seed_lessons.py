from django.core.management.base import BaseCommand, CommandError

from apps.cohorts.models import Track
from apps.lessons.models import Lesson

FRONTEND_LESSONS = [
    {
        "slug": "what-is-html",
        "title": "What is HTML?",
        "order": 1,
        "is_free": True,
        "summary": "The building blocks of every web page, explained from zero — what HTML is, what it isn't, and why it works the way it does.",
        "body": """
<p>Every web page you've ever visited — this one included — is built out of
HTML. Before we write any of it, it's worth being precise about what HTML
actually <em>is</em>, because the most common beginner confusion is
expecting it to behave like a programming language when it isn't one.</p>

<p>HTML is not a programming language. It has no <code>if</code>
statements, no math, no loops, no way to make a decision. What it <em>is</em>
is a <strong>markup language</strong> — a system for wrapping pieces of
content in <strong>tags</strong> that say what each piece <em>is</em>. You're
not telling the computer what to do, step by step; you're labelling things.
"This is a heading." "This is a paragraph." "This is a list." The browser
reads those labels and decides how to display each one.</p>

<h2>Why a "labelling" system, and not just plain text?</h2>
<p>Imagine you handed someone a page of plain text with no formatting at all
— no bold, no headings, no paragraph breaks — and asked them to figure out
which line was the title and which was body text. They'd have to guess from
context. A browser has the exact same problem: without labels, it has no
way to know a title from a footnote from a caption. HTML's whole job is to
remove that guesswork, for both the browser <em>and</em> anyone using
assistive technology like a screen reader, who relies entirely on those
labels to understand what's on the page at all.</p>

<h2>Example 1: the smallest possible page</h2>
<pre><code>&lt;h1&gt;Welcome&lt;/h1&gt;
&lt;p&gt;This is a paragraph of text.&lt;/p&gt;</code></pre>
<p>Here, <code>&lt;h1&gt;</code> labels "Welcome" as the single most
important heading on the page, and <code>&lt;p&gt;</code> labels the second
line as an ordinary paragraph. That's the entire pattern HTML runs on: a
piece of content, wrapped in a tag that names what it is.</p>

<h2>Example 2: the same idea, with a list</h2>
<pre><code>&lt;h2&gt;Things HTML can label&lt;/h2&gt;
&lt;ul&gt;
  &lt;li&gt;Headings&lt;/li&gt;
  &lt;li&gt;Paragraphs&lt;/li&gt;
  &lt;li&gt;Lists (like this one)&lt;/li&gt;
&lt;/ul&gt;</code></pre>
<p><code>&lt;ul&gt;</code> ("unordered list") labels a group of items as a
bulleted list, and each <code>&lt;li&gt;</code> ("list item") labels one
entry in it. Notice the pattern repeating: a container tag
(<code>&lt;ul&gt;</code>) holding smaller tags (<code>&lt;li&gt;</code>)
inside it. Almost all of HTML is built from nesting tags like this.</p>

<h2>Example 3: a label that isn't visible text at all</h2>
<pre><code>&lt;img src="cat.jpg" alt="A gray cat sleeping on a keyboard"&gt;</code></pre>
<p>Not every tag wraps text — <code>&lt;img&gt;</code> labels a spot on the
page as "an image goes here," and tells the browser where to find it. You'll
meet this one properly in the Links &amp; Images lesson, but it's worth
seeing early: the same "label what this is" idea applies to pictures,
videos, and interactive elements too, not just text.</p>

<h2>Tags come in pairs (mostly)</h2>
<p>Most tags have an opening tag (<code>&lt;p&gt;</code>) and a matching
closing tag (<code>&lt;/p&gt;</code>) with a forward slash. Whatever sits
between them is the content that label applies to. A few tags, like
<code>&lt;img&gt;</code> above, don't wrap anything and don't need a
closing tag at all — there's nothing "inside" an image.</p>

<h2>Common mistake: forgetting the closing tag</h2>
<p>Forget <code>&lt;/p&gt;</code> and the browser doesn't know where that
paragraph is supposed to end — it just keeps swallowing everything after
it into the same paragraph, which is why a whole page sometimes renders
looking subtly "wrong" with no error message anywhere. This is the single
most common beginner mistake in HTML, and now that you know to look for
it, it's usually a five-second fix: find the tag you opened, make sure it's
closed.</p>

<p>That's the whole idea HTML is built on. Everything from here is just
learning which specific tag to reach for — a heading, a table, a form, a
link — and that's exactly what the rest of this tutorial covers, one
concept at a time.</p>
""",
    },
    {
        "slug": "html-document-structure",
        "title": "HTML Document Structure",
        "order": 2,
        "is_free": True,
        "summary": "The skeleton every HTML file starts with — what each line does, why it exists, and what happens if you get it wrong.",
        "body": """
<p>Every HTML page starts with the same handful of lines before any real
content appears. Beginners often copy this skeleton without understanding
it, type it enough times that it becomes muscle memory, and never actually
learn what each line is for. Let's not do that — each line here exists to
solve a specific, real problem.</p>

<h2>Example 1: the full skeleton</h2>
<pre><code>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="UTF-8"&gt;
  &lt;title&gt;My Page&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Hello, world&lt;/h1&gt;
&lt;/body&gt;
&lt;/html&gt;</code></pre>

<h2>Line by line — what, and why</h2>
<ul>
<li><code>&lt;!DOCTYPE html&gt;</code> — this isn't even a real HTML tag;
it's an instruction to the browser that says "render this using the modern
HTML standard." Without it, older browsers fall back to a
compatibility mode from the 1990s that renders CSS inconsistently. It costs
nothing to include and prevents a whole category of "why does this look
different in different browsers" bugs.</li>
<li><code>&lt;html lang="en"&gt;</code> — the root element; every other tag
on the page lives inside this one. The <code>lang</code> attribute isn't
decorative — screen readers use it to choose the correct pronunciation
rules, and browsers use it to decide whether to offer a translation.
Setting it to the wrong language actively makes the page worse for those
users, so it's worth getting right rather than leaving as a placeholder.</li>
<li><code>&lt;head&gt;</code> — information <em>about</em> the page that
isn't shown directly on it: the page title, the character encoding, links
to CSS files, metadata for search engines and social media previews.
Nothing inside <code>&lt;head&gt;</code> is visible content.</li>
<li><code>&lt;body&gt;</code> — everything the visitor actually sees. Every
visible piece of content on the entire page goes here, and only here.</li>
</ul>

<h2>Example 2: what meta charset actually prevents</h2>
<pre><code>&lt;meta charset="UTF-8"&gt;</code></pre>
<p>This line tells the browser which set of characters to expect. Without
it, a browser has to guess — and guesses wrong often enough that you'll see
text like "café" rendered as "cafÃ©" on a real site somewhere. UTF-8 covers
essentially every character in every language, including emoji, so this
line is close to "always include it, never think about it again."</p>

<h2>Example 3: the title tag's two jobs</h2>
<pre><code>&lt;title&gt;Frontend Development · Code Secure Academy&lt;/title&gt;</code></pre>
<p><code>&lt;title&gt;</code> does two things at once: it's what shows in
the browser tab, and it's the headline Google shows in search results. A
page titled just "Home" tells a visitor and a search engine nothing about
what the page actually contains — a specific, descriptive title is one of
the cheapest improvements you can make to a real site.</p>

<h2>Why the head/body split matters in practice</h2>
<p>New developers sometimes paste visible content into <code>&lt;head&gt;</code>
by accident — a stray paragraph, an image — and the browser simply doesn't
show it, with no error to explain why. Once you know the rule (metadata in
<code>head</code>, visible content in <code>body</code>, no exceptions),
"my content just isn't showing up" becomes a five-second check instead of a
confusing mystery.</p>
""",
    },
    {
        "slug": "text-and-headings",
        "title": "Text & Headings",
        "order": 3,
        "is_free": True,
        "summary": "Headings, paragraphs, and basic text formatting — what each tag communicates, and why hierarchy matters more than size.",
        "body": """
<p>Most of what's on a typical web page is just text — but HTML gives you
several different tags for text, and each one communicates something
specific. Picking the right one isn't pedantry; it's what makes a page
usable by search engines, screen readers, and skimming humans alike.</p>

<h2>Example 1: the six heading levels</h2>
<pre><code>&lt;h1&gt;Code Secure Academy&lt;/h1&gt;
&lt;h2&gt;Our Tracks&lt;/h2&gt;
&lt;h3&gt;Frontend Development&lt;/h3&gt;
&lt;h3&gt;Backend Development&lt;/h3&gt;
&lt;h2&gt;Contact Us&lt;/h2&gt;</code></pre>
<p>HTML gives you six levels of heading, <code>&lt;h1&gt;</code> through
<code>&lt;h6&gt;</code>, from most important to least. A page should
normally have exactly <strong>one</strong> <code>&lt;h1&gt;</code> — its
main title — and then use <code>&lt;h2&gt;</code>, <code>&lt;h3&gt;</code>
and so on for sections and subsections underneath it, the same way a book
has one title, then chapters, then subheadings inside each chapter. In the
example above, notice "Frontend Development" and "Backend Development" are
both <code>&lt;h3&gt;</code> because they're both subsections of "Our
Tracks" — siblings at the same level get the same heading level.</p>

<h2>Why hierarchy, not just size</h2>
<p>It's tempting to pick a heading level purely by how big you want the
text to look on screen. Resist that — sizing is CSS's job entirely, and
heading levels exist to describe <em>structure</em>, not appearance. Two
concrete reasons this matters: screen readers let visually impaired users
jump directly between headings to navigate a page without reading every
word, the same way a sighted user skims a page visually — and search
engines use your heading structure to understand what a page is actually
about and how it's organized. Skip straight from an <code>&lt;h1&gt;</code>
to an <code>&lt;h4&gt;</code> because a particular size "looked right," and
you've quietly broken that structure for both audiences at once, with
nothing on screen looking obviously wrong to you.</p>

<h2>Example 2: paragraphs and basic emphasis</h2>
<pre><code>&lt;p&gt;Regular text goes in a paragraph tag.
Use &lt;strong&gt;strong&lt;/strong&gt; for text that's genuinely
important, and &lt;em&gt;em&lt;/em&gt; for emphasis.&lt;/p&gt;</code></pre>
<p><code>&lt;strong&gt;</code> and <code>&lt;em&gt;</code> aren't just
"bold" and "italic" wearing different names — browsers do render them that
way by default, but their real job is meaning, not appearance. A screen
reader will actually change its tone of voice for them, which a plain
CSS-only bold or italic style never triggers. If you just want something to
<em>look</em> bold with no real emphasis meant (a logo, a stylistic choice),
that's a job for CSS's <code>font-weight</code>, not <code>&lt;strong&gt;</code>.</p>

<h2>Example 3: line breaks vs. new paragraphs</h2>
<pre><code>&lt;p&gt;123 Main Street&lt;br&gt;Lagos, Nigeria&lt;/p&gt;
&lt;p&gt;A completely separate paragraph.&lt;/p&gt;</code></pre>
<p><code>&lt;br&gt;</code> forces a line break <em>within</em> the same
paragraph — useful for something like a postal address, where the lines
are related but not separate thoughts. A new <code>&lt;p&gt;</code>, by
contrast, is a genuinely new paragraph. Using a string of
<code>&lt;br&gt;&lt;br&gt;</code> tags to fake paragraph spacing (a common
shortcut) loses the actual structural meaning that "these are two separate
paragraphs" — use two <code>&lt;p&gt;</code> tags instead, and let CSS
control the spacing between them.</p>

<h2>Common mistake: choosing headings for their size, not their level</h2>
<p>If a heading "looks too big," the fix is CSS (<code>font-size</code>),
never dropping down to a lower heading tag just to shrink it. Keep the tag
that correctly describes the content's structure, and control how it looks
separately — this is exactly the same content-vs-appearance split you saw
in the very first lesson, and it comes up constantly throughout HTML.</p>
""",
    },
    {
        "slug": "links-and-images",
        "title": "Links & Images",
        "order": 4,
        "is_free": False,
        "summary": "How pages connect to each other, how to embed images correctly, and the small details that separate a good link/image from a broken or inaccessible one.",
        "body": """
<p>Links are what make the web a <em>web</em> in the first place — pages
connected to other pages. Images are what make a page feel real instead of
a wall of text. Both are simple to use, but each has a couple of details
that are easy to miss and genuinely matter.</p>

<h2>Example 1: an absolute link</h2>
<pre><code>&lt;a href="https://example.com"&gt;Visit example.com&lt;/a&gt;</code></pre>
<p>You create a link with an <code>&lt;a&gt;</code> tag (short for "anchor")
and an <code>href</code> attribute pointing at the destination. This one is
<strong>absolute</strong> — a full, complete address to somewhere else on
the internet, including the <code>https://</code> part.</p>

<h2>Example 2: a relative link</h2>
<pre><code>&lt;a href="/about"&gt;About us&lt;/a&gt;</code></pre>
<p>This link is <strong>relative</strong> — it means "the <code>/about</code>
page on this <em>same</em> site," with no domain written out at all. This
is what you'll use for links within your own project, and there's a
concrete reason why: a relative link keeps working no matter what domain
the site ends up deployed to — localhost while you're building it, then a
real domain later — without you needing to go back and change a single
link. An absolute link to your own site's pages would break (or silently
point at the wrong environment) the moment the domain changed.</p>

<h2>Example 3: opening a link in a new tab, safely</h2>
<pre><code>&lt;a href="https://example.com" target="_blank" rel="noopener"&gt;
  Visit example.com
&lt;/a&gt;</code></pre>
<p><code>target="_blank"</code> opens the link in a new tab instead of
navigating away from your page. Always pair it with
<code>rel="noopener"</code> — without it, the page you just linked to gets
a small amount of programmatic access back to your original tab (it can,
for example, silently redirect it to a phishing look-alike while the user
is looking at the new tab). It's a real, if narrow, security gap, and
<code>rel="noopener"</code> closes it completely at zero cost — worth
making a permanent habit rather than something you remember only
sometimes.</p>

<h2>Example 4: an image, done properly</h2>
<pre><code>&lt;img src="cat.jpg" alt="A gray cat sleeping on a keyboard" width="400"&gt;</code></pre>
<p>Every <code>&lt;img&gt;</code> needs at minimum <code>src</code> (where
the image file actually is) and <code>alt</code> (a text description of
what the image shows). <code>alt</code> is not optional decoration — it's
what a screen reader announces out loud instead of the image, and it's what
displays as fallback text if the image fails to load (a slow connection, a
typo'd filename, a deleted file). A missing or lazy <code>alt=""</code> on
an image that actually conveys information is one of the single most common
accessibility mistakes on the entire web, and — unlike a lot of
accessibility work — it's genuinely one of the cheapest to get right: you
just have to remember to describe what you're looking at.</p>

<h2>When alt text should be empty on purpose</h2>
<p>Not every image needs a description. A purely decorative image — a
background flourish that conveys no information on its own — should use
<code>alt=""</code> (present, but deliberately empty) so a screen reader
skips over it silently instead of announcing something meaningless like
"decorative border image." The rule of thumb: if removing the image would
lose information, describe it; if removing it would lose nothing, mark it
as decorative on purpose.</p>

<h2>Common mistake: writing alt text that just repeats "image of..."</h2>
<p>Alt text like <code>alt="image"</code> or <code>alt="picture of a cat"</code>
tells a screen reader user almost nothing useful — they already know it's
an image, that's why the screen reader is describing it. Write what the
image actually <em>shows</em> and, if relevant, why it's there: <code>alt="A
gray cat sleeping on a keyboard"</code> tells a real story; <code>alt="cat
image"</code> doesn't.</p>
""",
    },
    {
        "slug": "forms-and-inputs",
        "title": "Forms & Inputs",
        "order": 5,
        "is_free": False,
        "summary": "How to collect input from a visitor — the basis of every signup, login, and contact form — and why the details (labels, input types, required) each pull real weight.",
        "body": """
<p>Nearly every interactive site — including this one — relies on forms:
signup, login, checkout, contact. A form wraps a set of inputs and, on
submit, sends their values somewhere for a server to process. The markup
looks simple, but three small details separate a form that's genuinely
usable from one that just "looks" fine.</p>

<h2>Example 1: a minimal, complete form</h2>
<pre><code>&lt;form action="/submit" method="post"&gt;
  &lt;label for="email"&gt;Email&lt;/label&gt;
  &lt;input type="email" id="email" name="email" required&gt;

  &lt;button type="submit"&gt;Send&lt;/button&gt;
&lt;/form&gt;</code></pre>
<p><code>action</code> says where the form's data gets sent, and
<code>method="post"</code> says how (POST is the standard choice for
anything that changes data — a signup, a purchase — rather than just
reading it).</p>

<h2>Why the label/input connection isn't optional</h2>
<p>The <code>&lt;label for="email"&gt;</code> is tied to the input sharing
that exact same <code>id="email"</code>. This connection does two real
things: clicking anywhere on the label text focuses the input (try it —
click "Email" above and the cursor jumps into the box), and — more
importantly — a screen reader announces that label out loud when the user
tabs into the field. A form built with placeholder text standing in for a
real <code>&lt;label&gt;</code> might look identical to a sighted user, but
it's genuinely difficult or impossible for a screen reader user to fill
out correctly, since placeholder text disappears the moment you start
typing and isn't reliably announced the same way a label is.</p>

<h2>Example 2: input types that do real work for you</h2>
<pre><code>&lt;input type="email" name="email"&gt;
&lt;input type="password" name="password"&gt;
&lt;input type="tel" name="phone"&gt;
&lt;input type="checkbox" name="subscribe"&gt; Subscribe to updates</code></pre>
<p>HTML has far more input types than most beginners realize, and each one
earns its keep:</p>
<ul>
<li><code>type="email"</code> — on mobile, the keyboard that pops up
includes an @ key; the browser also validates the value is email-shaped
before your own code ever sees it.</li>
<li><code>type="password"</code> — masks each character as it's typed, so
it's not visible over someone's shoulder.</li>
<li><code>type="tel"</code> — brings up a numeric phone keypad on mobile
instead of a full keyboard, a small thing that makes a real difference to
how fast someone can fill the field in.</li>
<li><code>type="checkbox"</code> / <code>type="radio"</code> — checkboxes
let someone pick any number of options from a set (including none);
radio buttons (sharing the same <code>name</code>) restrict the choice to
exactly one.</li>
</ul>
<p>Using <code>type="text"</code> for all of these would technically "work"
— the form would still submit — but you'd lose every one of these free
behaviors the browser hands you for choosing the right type.</p>

<h2>Example 3: the required attribute</h2>
<pre><code>&lt;input type="email" name="email" required&gt;</code></pre>
<p><code>required</code> stops the form from submitting at all until that
field has something in it, and the browser shows its own built-in
validation message — a first line of defense against empty submissions
that costs you zero lines of code. It is <strong>not</strong> a substitute
for checking the data again on the server: browser validation is easy for
anyone to bypass (disable JavaScript, edit the HTML, or just send a raw
request straight to your server without using the form at all), so a real
application always re-validates on the server too. Think of
<code>required</code> as a courtesy to honest users filling out the form
normally, not a security boundary.</p>

<h2>Common mistake: a form with no visible way to know it worked</h2>
<p>A form that submits but gives no confirmation — no success message, no
redirect, no visible change — leaves the visitor unsure whether anything
happened at all, and a nervous user will often just click "Send" again,
sometimes submitting the same data twice. Always give a form some clear
next step after submission: a thank-you message, a redirect to a
confirmation page, something. It's a small detail, but it's the difference
between a form that feels finished and one that feels broken even when the
underlying code is working fine.</p>
""",
    },
]

BACKEND_LESSONS = [
    {
        "slug": "what-is-backend-development",
        "title": "What is Backend Development?",
        "order": 1,
        "is_free": True,
        "summary": "The server-side half of every app — what it actually does, why it's invisible, and a mental model that makes the rest of this track click.",
        "body": """
<p>If frontend is everything a visitor sees and clicks, backend is
everything running on a server that they never see directly: storing
data, checking passwords, deciding what a request is even allowed to do.
When you type your password into a login form, your browser has no idea
whether it's correct — it sends it to a backend server, which checks it
against a database and sends back a plain yes or no.</p>

<h2>Why a "backend" exists at all</h2>
<p>You might wonder why the browser can't just do everything itself. The
answer is trust: a browser runs entirely on the visitor's own computer,
which means the visitor (or anyone technical enough) can inspect and
change anything running there. If "you're logged in as admin" were a fact
your browser decided on its own, anyone could just tell their browser to
decide that. A backend runs somewhere the visitor can't reach or tamper
with, which is what makes it possible to trust its answers at all.</p>

<h2>Example 1: three things almost every backend handles</h2>
<ul>
<li>Talking to a <strong>database</strong> — storing and retrieving data
that has to survive after the server restarts.</li>
<li>Exposing an <strong>API</strong> — a fixed set of URLs other programs
(including your own frontend) can call to read or change that data.</li>
<li>Enforcing <strong>rules</strong> — you can't read someone else's
private messages, you can't check out a shopping cart that isn't yours,
even if you know the right URL to try it.</li>
</ul>

<h2>Example 2: a mental model worth keeping</h2>
<p>Picture a restaurant. The frontend is the dining room — what customers
see, sit in, and interact with directly. The backend is the kitchen:
customers never enter it, but nothing on their plate exists without it.
A waiter (the API) carries orders in and plates back out, and never
improvises a dish on their own — they follow what the kitchen actually
prepared. That's a genuinely useful way to think about almost any web
app: the frontend requests, the backend decides and prepares, and a
well-defined channel (the API) carries information between the two.</p>

<h2>Why this split matters in practice</h2>
<p>Splitting frontend and backend means each can change independently — a
backend team can swap their database engine or rewrite how prices are
calculated without the frontend needing to know or care, as long as the
API between them stays the same. That independence is a big part of why
almost every real company organizes its engineering this way, and it's
exactly the boundary the next few lessons explore.</p>
""",
    },
    {
        "slug": "requests-and-responses",
        "title": "How the Web Talks: Requests & Responses",
        "order": 2,
        "is_free": True,
        "summary": "The request/response cycle underneath every click, form submit, and API call — and why reading a status code is the fastest way to debug almost anything.",
        "body": """
<p>Every time a browser loads a page, submits a form, or a frontend calls
an API, the exact same basic exchange happens: the client sends a
<strong>request</strong>, the server sends back a
<strong>response</strong>. This exchange, and the rules it follows, is
called HTTP — and it's the protocol the entire web runs on, from the
simplest static page to the most complex app.</p>

<h2>Example 1: anatomy of a request</h2>
<pre><code>GET /api/students/42 HTTP/1.1
Host: codesecureacademy.com
Authorization: Bearer eyJhbGciOi...</code></pre>
<p>Three parts worth knowing by name: a <strong>method</strong> saying
what kind of action this is (<code>GET</code> to read data,
<code>POST</code> to create something new, <code>PUT</code>/<code>PATCH</code>
to update, <code>DELETE</code> to remove), a <strong>path</strong> saying
which specific thing the request is about, and <strong>headers</strong>
carrying metadata like who's asking (here, an authentication token).</p>

<h2>Example 2: anatomy of a response</h2>
<pre><code>HTTP/1.1 200 OK
Content-Type: application/json

{"id": 42, "name": "Ada", "track": "Backend"}</code></pre>
<p>A <strong>status code</strong> — that <code>200</code> — tells the
client what happened before it even reads a single byte of the body:
<code>200</code> means success, <code>404</code> means "nothing exists at
that path," <code>401</code> means "you're not logged in,"
<code>500</code> means the server itself broke while handling the
request. Learning to read status codes before anything else is genuinely
one of the fastest ways to debug a broken API call — the number alone
usually tells you which side of the conversation the problem is on.</p>

<h2>Example 3: the same request, three different outcomes</h2>
<pre><code>GET /api/students/42   -> 200 OK           (student exists, here it is)
GET /api/students/9999 -> 404 Not Found    (no student with that id)
GET /api/students/42   -> 401 Unauthorized (missing/expired login token)</code></pre>
<p>Same path, same method — but the response tells three completely
different stories depending on what's actually true on the server. This
is the entire reason status codes exist: so the client doesn't have to
guess what happened by parsing the response body.</p>

<h2>Why this matters for everything that follows</h2>
<p>Every backend framework — Django, Laravel, Flask, Express, whatever
you eventually reach for — is really just a structured way of saying
"when a request like <em>this</em> arrives, run <em>this</em> code and
send back <em>this</em> response." Once that request/response cycle
genuinely clicks, the rest of backend development is mostly variations on
it: different paths, different logic, different data — same underlying
shape every time.</p>
""",
    },
    {
        "slug": "databases-101",
        "title": "Databases 101",
        "order": 3,
        "is_free": True,
        "summary": "Why almost every backend needs somewhere to durably store data, how that data gets organized, and why a plain file isn't good enough.",
        "body": """
<p>A backend without a database forgets everything the moment it
restarts — every signup, every order, every message, gone. A
<strong>database</strong> is where that data lives permanently, organized
in a way that makes it fast to search, safe to update, and reliable even
when many things are happening to it at once.</p>

<h2>Example 1: tables, rows, columns</h2>
<pre><code>students
id | name  | track
1  | Ada   | Backend
2  | Chidi | Cybersecurity
3  | Musa  | Frontend</code></pre>
<p>A relational database (the most common kind — Postgres, MySQL, SQLite)
organizes data into <strong>tables</strong>, a bit like a spreadsheet:
each <strong>column</strong> is a named field every row shares (
<code>name</code>, <code>track</code>), and each <strong>row</strong> is
one actual record — one real student.</p>

<h2>Example 2: relationships between tables</h2>
<pre><code>tracks
id | name
1  | Backend
2  | Cybersecurity

students
id | name  | track_id
1  | Ada   | 1
2  | Chidi | 2</code></pre>
<p>Real data connects across tables — a student belongs to a track, an
order belongs to a customer. Rather than repeating a track's full name
and description inside every single student row, a table stores a small
reference (a <strong>foreign key</strong> — here, <code>track_id</code>)
pointing at the related row in another table. This is what makes a
database <em>relational</em>, and it's exactly why backend frameworks
ship an <strong>ORM</strong> (Object-Relational Mapper) — a layer that
lets you work with these connected records using your programming
language's normal syntax, instead of hand-writing SQL joins by hand every
single time you need related data.</p>

<h2>Why not just use a text file?</h2>
<p>A database earns its complexity by solving problems a plain file
genuinely can't handle safely: many requests reading and writing at the
exact same moment without corrupting each other's changes, fast lookups
even across millions of rows (a text file search gets slower the bigger
it gets; a well-indexed database mostly doesn't), and rules that reject
bad data automatically before it's ever saved — a column defined as "must
be a number" simply refuses a row that tries to save text into it.
That reliability, largely invisible when everything's working, is most
of what you're actually paying for in complexity when you reach for a
real database instead of rolling your own file-based storage.</p>
""",
    },
    {
        "slug": "building-a-simple-api",
        "title": "Building a Simple API",
        "order": 4,
        "is_free": False,
        "summary": "Turning a database table into endpoints a frontend can actually call — and why the server, not the browser, is where real validation has to live.",
        "body": """
<p>An API is a contract: a fixed set of URLs a client can call, each
doing exactly one predictable thing. A typical resource gets a small,
consistent set of endpoints, mapped straight onto the HTTP methods from
the requests-and-responses lesson.</p>

<h2>Example 1: a full CRUD set for one resource</h2>
<pre><code>GET    /api/posts      -> list every post
POST   /api/posts      -> create a new post
GET    /api/posts/5    -> fetch one specific post
PATCH  /api/posts/5    -> update part of that post
DELETE /api/posts/5    -> delete it</code></pre>
<p>Notice the pattern: the <em>path</em> says which resource, and the
<em>method</em> says what to do to it. This four-or-five-endpoint shape
(often called CRUD — Create, Read, Update, Delete) covers a huge share of
what real APIs actually do.</p>

<h2>Example 2: status codes, done right</h2>
<pre><code>POST /api/posts          -> 201 Created   (successfully made a new one)
GET  /api/posts/999      -> 404 Not Found (id 999 doesn't exist)
POST /api/posts (bad data)-> 400 Bad Request (validation failed)</code></pre>
<p>A well-built API doesn't just return <code>200</code> for everything
and let the client figure out what actually happened by reading the body.
Creating something new should return <code>201 Created</code>; a request
for something that doesn't exist should return <code>404</code>, not a
generic crash; bad input should return <code>400</code> with a message
saying what was wrong. Getting this right is what separates an API that's
genuinely pleasant to build a frontend against from one that turns every
integration into a guessing game.</p>

<h2>Why validation has to happen on the server, not just the frontend</h2>
<p>A frontend form can check that an email field looks like an email
before it's even submitted — but that check is only ever a convenience
for honest users filling out the form the normal way. Nothing stops
someone from calling your API directly with a tool like curl or Postman,
skipping your frontend's form entirely and sending whatever raw data they
want. If the server doesn't independently check it too, it genuinely
isn't checked at all — the frontend's validation is a courtesy, not a
security boundary, no matter how thorough it looks.</p>

<p>This lesson is a locked preview — the full track walks through
building and testing a real API end to end, wiring it to a database, and
deploying it somewhere real traffic can actually reach it.</p>
""",
    },
    {
        "slug": "authentication-and-sessions",
        "title": "Authentication & Sessions",
        "order": 5,
        "is_free": False,
        "summary": "How a backend remembers who you are across many separate requests, the two common ways to do it, and why getting this wrong is uniquely costly.",
        "body": """
<p>HTTP is <strong>stateless</strong> — by default, the server treats
every single request as if it's never seen you before, with zero built-in
memory of the last one. So how does a site know you're still logged in
when you click through to a new page a minute later? It needs you to
prove your identity on every request, without literally asking for your
password again and again.</p>

<h2>Example 1: session-based auth</h2>
<pre><code>1. You log in with your password.
2. Server creates a session record: { user: "ada", expires: ... }
3. Server sends your browser a cookie containing just the session's id.
4. Every later request, your browser auto-attaches that cookie.
5. Server looks up the id, finds the session, knows it's you.</code></pre>
<p>The server does the remembering here — the cookie itself is just a
lookup key, meaningless without the matching session record sitting on
the server.</p>

<h2>Example 2: token-based auth (e.g. JWT)</h2>
<pre><code>1. You log in with your password.
2. Server creates a signed token containing your identity directly:
   { user: "ada", expires: ... } + a cryptographic signature.
3. Client stores the token and attaches it to every request's
   Authorization header.
4. Server verifies the signature — no database lookup needed at all.</code></pre>
<p>The difference from sessions: the token carries the actual information
inside it, cryptographically signed so it can't be edited undetected. No
per-request database lookup is needed to check it, which is a real
performance win — part of why APIs consumed by mobile apps, which may
talk to several different backend servers, often prefer this approach
over sessions.</p>

<h2>Why this is a uniquely security-critical lesson</h2>
<p>Getting authentication wrong is one of the most common — and most
damaging — categories of mistake in backend development: accidentally
leaking one user's session to another, trusting a token's contents
without actually verifying its cryptographic signature, or storing
passwords in plain, readable text instead of a proper one-way hash. Every
one of these is a real, specific mistake real companies have shipped to
production. This is exactly the kind of thing the full track spends real,
supervised practice time on, since a small mistake here doesn't
compromise one account — it can compromise every account on the system at
once.</p>
""",
    },
]

CYBERSECURITY_LESSONS = [
    {
        "slug": "what-is-cybersecurity",
        "title": "What is Cybersecurity?",
        "order": 1,
        "is_free": True,
        "summary": "The roles, goals, and daily reality of working in security — and why it's a field, not a single job.",
        "body": """
<p>Cybersecurity is the practice of protecting systems, networks, and
data from people trying to break into, damage, or steal them. It's less
one job than a whole field of specialties, each solving a different piece
of the same overall problem.</p>

<h2>Example 1: three roles, three different jobs</h2>
<ul>
<li>A <strong>SOC analyst</strong> (Security Operations Center) watches
live traffic and alerts, deciding in real time whether something odd is
actually an attack.</li>
<li>A <strong>penetration tester</strong> is paid, with explicit written
permission, to break into a system on purpose so the holes get fixed
before a real attacker finds them.</li>
<li>A <strong>security engineer</strong> builds the defenses everyone
else — including the two roles above — actually relies on: firewalls,
secure configurations, safe coding practices.</li>
</ul>
<p>These aren't competing job titles; a real security team usually needs
all three, since watching for attacks, testing for weaknesses, and
building defenses are three genuinely different skills.</p>

<h2>What the job actually looks like day to day</h2>
<p>Despite the movie version, most security work isn't a dramatic
last-minute keyboard duel against a countdown timer — it's careful and
methodical: reading logs line by line, checking a configuration file
against a known-safe baseline, testing whether a fix actually closed a
hole or just moved it somewhere less obvious. The skill that matters most
isn't memorizing every tool that exists; it's a particular way of
thinking about systems, which the very next lesson covers directly.</p>

<h2>Why it matters more every year</h2>
<p>Nearly everything — banking, healthcare records, elections
infrastructure, the platform you're reading this on right now — runs on
software. Every one of those systems has to be actively defended by
someone, continuously, since attackers only need one gap while defenders
have to cover all of them. That asymmetry is exactly why demand for
security skills keeps growing faster than most other areas of tech.</p>
""",
    },
    {
        "slug": "think-like-an-attacker",
        "title": "Think Like an Attacker",
        "order": 2,
        "is_free": True,
        "summary": "The mindset shift that underlies every security skill you'll build in this track.",
        "body": """
<p>The single most useful habit in security is looking at a working
system and asking: "if I wanted to break this, where would I try first?"
Defenders who only think about how a system is <em>supposed</em> to work
miss the paths an attacker actually takes — precisely the paths the
system was never designed to expect.</p>

<h2>Example 1: one login form, two completely different mindsets</h2>
<p>A login form checks a username and password against a database. The
"intended" use is typing a real username and a real password. An
attacker asks a different set of questions instead: What happens if I
submit a username that's absurdly long? What if the password field also
happens to accept a database command instead of plain text? What happens
if I just try a thousand passwords a second against the same account?
None of these are how the form was "meant" to be used — which is exactly
why each one is worth checking before someone else does.</p>

<h2>Example 2: reconnaissance comes before any actual attack</h2>
<p>Before touching a system at all, attackers — and, in an authorized
test, security professionals doing the same thing legally — spend real
time just gathering information: what software is running, what's
publicly exposed to the internet, what employees have posted online that
might hint at internal systems or habits. Most real attacks don't open
with a clever exploit; they open with patient information-gathering that
quietly reveals an easier way in than brute force ever would.</p>

<h2>Why this mindset is defensive, not just offensive</h2>
<p>You don't need to intend to attack anything to genuinely benefit from
thinking this way. The best defenders constantly ask "how would this
actually be abused?" about their <em>own</em> systems — their own login
form, their own API, their own file uploads — and fix what they find
before anyone else has the chance to.</p>
""",
    },
    {
        "slug": "passwords-and-authentication",
        "title": "Your First Line of Defense: Passwords & Authentication",
        "order": 3,
        "is_free": True,
        "summary": "Why most real-world breaches start here, and what genuinely helps versus what only feels like it helps.",
        "body": """
<p>An enormous share of real breaches don't involve a clever technical
exploit at all — they involve a guessed, reused, or outright stolen
password. This is why authentication is one of the very first things any
security-minded person learns to take seriously, both to defend and,
later in this track, to responsibly test.</p>

<h2>Example 1: what actually makes a password strong</h2>
<pre><code>Weak (looks complex, isn't):   P@ssw0rd!
Strong (long, unpredictable):  correct-horse-battery-staple-42</code></pre>
<p><strong>Length beats complexity.</strong> A long, random passphrase is
far harder to crack than a short password with a few symbols swapped
in — attacker cracking tools already expect substitutions like "@" for
"a" and "0" for "o", so they barely slow an attack down. A password
manager is what makes it realistic to actually use a unique, long
password on every single site, instead of reusing one you can remember.</p>

<h2>Example 2: multi-factor authentication (MFA)</h2>
<pre><code>Password alone:        knowing the password = full access
Password + MFA:        knowing the password = still needs a second proof
                        (a code from your phone, a hardware key, a fingerprint)</code></pre>
<p>Even if a password leaks — and passwords leak constantly, in breaches
that may have nothing to do with you personally — MFA stops that leaked
password from being enough on its own to get in. It's genuinely the
single highest-impact step most individuals and organizations can take,
for a relatively small amount of daily friction.</p>

<h2>Example 3: three common attacks against passwords</h2>
<ul>
<li><strong>Brute-force</strong> — systematically trying every possible
password combination until one works.</li>
<li><strong>Credential stuffing</strong> — taking passwords already
leaked from one breached site and trying them against other unrelated
sites, betting (correctly, most of the time) that people reuse
passwords.</li>
<li><strong>Phishing</strong> — skipping the guessing entirely and just
asking for the password directly, disguised as something legitimate.</li>
</ul>
<p>Understanding these three specifically is the foundation the hands-on
penetration testing lessons later in this track build directly on top of.</p>
""",
    },
    {
        "slug": "introduction-to-penetration-testing",
        "title": "Introduction to Penetration Testing",
        "order": 4,
        "is_free": False,
        "summary": "Getting paid, authorized permission to break into systems — so someone else can't do it without permission first.",
        "body": """
<p>A penetration test ("pentest") is an authorized, tightly scoped
attempt to break into a system, so its owner learns about real weaknesses
before an actual attacker does. The word <strong>authorized</strong> is
doing enormous work in that sentence — the exact same technical actions
are a serious crime without explicit written permission, and a paid,
respected profession with it.</p>

<h2>Example: the general shape of an engagement</h2>
<pre><code>1. Reconnaissance  — learn about the target, strictly within agreed scope
2. Scanning        — find what's actually reachable, and what it's running
3. Exploitation    — attempt to actually get in, ethically and in-scope
4. Reporting       — write up exactly what was found and how to fix it</code></pre>
<p>Beginners often assume step 3 is the whole job. In practice, step 4 —
<strong>reporting</strong> — is just as important: a vulnerability nobody
can act on because the write-up is unclear or missing key detail hasn't
actually helped anyone, no matter how impressive the exploit was.</p>

<h2>Why scope matters so much</h2>
<p>A pentest engagement defines, in writing, exactly what's in bounds and
what isn't — which systems, which techniques, which time window.
Stepping outside that agreed scope, even by accident, turns authorized
work into something else entirely in the eyes of the law. Respecting
scope is one of the very first professional habits this track builds,
deliberately before any tooling at all.</p>

<p>This lesson is a locked preview — the full track includes hands-on
labs in a safe, legal practice environment built specifically for this.</p>
""",
    },
    {
        "slug": "networking-fundamentals-for-security",
        "title": "Networking Fundamentals for Security",
        "order": 5,
        "is_free": False,
        "summary": "IP addresses, ports, and protocols — the map every security tool assumes you already have before its output makes any sense.",
        "body": """
<p>Almost every security tool assumes you already understand how data
actually moves between machines. Without that map, a tool's output is
just noise; with it, the exact same output tells a clear, specific story.</p>

<h2>Example 1: IP addresses and ports</h2>
<pre><code>Target: 203.0.113.10
Port 80  -> open (HTTP web server)
Port 443 -> open (HTTPS web server)
Port 22  -> open (SSH remote access)
Port 3306 -> closed (MySQL database, not exposed)</code></pre>
<p>An <strong>IP address</strong> identifies a specific machine on a
network. A <strong>port</strong> identifies a specific service running on
that machine — a web server usually listens on port 443 (HTTPS) or 80
(HTTP), remote administrative access typically on port 22 (SSH). Scanning
which ports are open on a target is often the very first technical step
in an authorized security assessment, because it reveals what's actually
running and reachable right now — not just what's supposed to be, which
is frequently a different, more revealing answer.</p>

<h2>Example 2: a few protocols worth knowing by name</h2>
<ul>
<li><strong>TCP</strong> — a reliable, connection-based way to send data;
most ordinary web traffic runs on it.</li>
<li><strong>DNS</strong> — translates a human-readable domain name like
<code>codesecureacademy.com</code> into the actual IP address a machine
needs to connect to.</li>
<li><strong>HTTPS</strong> — wraps ordinary HTTP traffic in encryption
(TLS), so it can't be read or silently tampered with while in transit.</li>
</ul>
<p>That last point is exactly why an unencrypted HTTP login form is a
real, checkable finding in a professional security assessment, not a
theoretical concern — anyone on the same network path can read what's
being typed into it.</p>

<h2>Why this belongs before the hands-on tools</h2>
<p>Every scanning and exploitation tool covered later in this track is
really just a structured, automated way of interacting with the concepts
on this page. The full track builds real, supervised hands-on practice
with this firsthand, on infrastructure built specifically for legal,
safe practice.</p>
""",
    },
]

GRAPHIC_DESIGN_LESSONS = [
    {
        "slug": "what-is-graphic-design",
        "title": "What is Graphic Design?",
        "order": 1,
        "is_free": True,
        "summary": "Design as problem-solving, not decoration.",
        "body": """
<p>Graphic design is the practice of communicating an idea visually —
through layout, color, type, and imagery — so it's understood instantly
and correctly. A good logo, a readable poster, an app icon someone
recognizes at a glance: all of it is design solving a specific
communication problem, not just "making things look nice."</p>

<h2>Example: judging a design by whether it works, not just how it looks</h2>
<p>Every real design brief starts with a question, not a blank canvas:
who is this for, what should they understand or feel, what should they
do next? Take a flyer for a live event: a version with a beautiful
photo and elegant type that buries the actual date and location in tiny
text has <em>failed at its job</em>, no matter how good it looks in a
portfolio. A plainer flyer where the date, location, and how to register
jump out immediately has succeeded, even with far less visual polish.
Judging your own work by "does this work for its purpose" — not just "do
I like how this looks" — is the single biggest shift between a hobbyist
and a working designer.</p>

<h2>Why the tools are secondary</h2>
<p>Figma, Photoshop, Illustrator — these are just how design gets
executed, and which specific tool is "standard" changes over the years
(Figma itself didn't exist fifteen years ago). The underlying skills —
composition, color, typography, hierarchy — transfer across every tool
you'll ever use for the rest of your career, which is exactly why this
track spends real time on them first, before diving deep into any one
piece of software.</p>
""",
    },
    {
        "slug": "elements-of-design",
        "title": "The Elements of Design: Color, Type & Space",
        "order": 2,
        "is_free": True,
        "summary": "The basic visual vocabulary every design decision is made from — four ideas that explain most of what separates a polished design from an amateur one.",
        "body": """
<p>Every design, however complex, is built from a small set of basic
elements. Learning to name them precisely is what lets you actually talk
about — and deliberately control — what makes a design work, instead of
just reacting to whether something "feels right."</p>

<h2>Element 1: Color</h2>
<p>Color sets mood and draws the eye before a viewer has read a single
word of text. A palette built from just two or three deliberately chosen
colors almost always reads as more professional than one with five
competing colors fighting for attention — restraint, not variety, is
usually the sign of an intentional choice.</p>

<h2>Element 2: Typography</h2>
<p>The typeface and sizing you choose carries its own tone entirely apart
from the words themselves — a rounded, friendly font says something
different from a sharp, geometric one, even displaying identical text.
Consistent type sizing (a small, deliberate set of sizes reused
throughout a design, rather than a slightly different size for every
single element) is one of the fastest ways to make a design read as
intentional rather than assembled piece by piece.</p>

<h2>Element 3: Space</h2>
<p><strong>Whitespace</strong> (the empty space around and between
elements) isn't wasted space — it's what lets a viewer's eye rest, and
what visually signals which elements belong together as a group versus
which are separate. Beginners often try to fill every available inch;
experienced designers actively protect empty space, because crowding
elements together with no breathing room is one of the fastest ways to
make an otherwise good design feel amateur.</p>

<h2>Element 4: Hierarchy</h2>
<p>Hierarchy means deliberately using size, weight, and position to
control the order a viewer's eye moves through a design — what they see
first, second, third. A design with no hierarchy at all — everything the
same size and weight — forces the viewer to do the work of figuring out
what matters most. Good hierarchy does that work <em>for</em> them,
before they've consciously thought about it.</p>

<h2>Why these four together, not separately</h2>
<p>These elements aren't independent choices — they reinforce each
other. A strong color accent draws attention to whatever already has
strong hierarchy; generous whitespace makes a clear typographic scale
even easier to read. The rest of this track is largely about learning to
use all four together on purpose, rather than in isolation.</p>
""",
    },
    {
        "slug": "understanding-color-theory",
        "title": "Understanding Color Theory",
        "order": 3,
        "is_free": True,
        "summary": "How colors relate to each other on the color wheel, a reliable formula for picking a palette, and why contrast isn't optional.",
        "body": """
<p>Color theory isn't about memorizing a wheel for its own sake — it's a
practical, repeatable way to predict which color combinations will feel
harmonious <em>before</em> you commit real design time to them.</p>

<h2>Example 1: three reliable color-wheel relationships</h2>
<ul>
<li><strong>Complementary</strong> colors sit directly opposite each
other on the wheel (blue and orange) — high contrast and energetic, but
easy to overdo if both are used at full strength everywhere.</li>
<li><strong>Analogous</strong> colors sit next to each other (blue, teal,
green) — naturally harmonious and calmer, since they share an underlying
hue family.</li>
<li><strong>Monochromatic</strong> palettes use different shades and
tints of a single color — the safest starting palette for a beginner,
since nothing within one hue family can visually clash with itself.</li>
</ul>

<h2>Example 2: a simple, reliable palette formula</h2>
<pre><code>60% — dominant color   (backgrounds, large areas)
30% — supporting color (secondary sections, cards)
10% — accent color     (buttons, highlights — used sparingly on purpose)</code></pre>
<p>This 60/30/10 split is a genuinely useful default whenever you're not
sure where to start: pick one dominant color, one clearly supporting
color, and reserve a single accent color exclusively for the things you
most want a viewer's eye drawn to — since an accent used everywhere stops
functioning as an accent at all.</p>

<h2>Why contrast isn't optional</h2>
<p>Text needs enough contrast against its background to actually be
readable in practice — light gray text on a white background might look
elegant and understated in a polished mockup, and be genuinely
unreadable for a real visitor, especially anyone with low vision or
using a phone screen outdoors in bright sunlight. Checking contrast
(dedicated tools exist that measure this precisely, giving a pass/fail
number rather than a guess) is a basic, table-stakes accessibility habit
for any working designer, not an advanced optional extra.</p>
""",
    },
    {
        "slug": "typography-fundamentals",
        "title": "Typography Fundamentals",
        "order": 4,
        "is_free": False,
        "summary": "Choosing and pairing typefaces like a working designer, with a real, testable effect on how long someone keeps reading.",
        "body": """
<p>Typography is often the single biggest lever on whether a design
feels professional or amateur — and it's also one of the most
under-studied skills among beginners, who tend to spend most of their
attention on color and imagery instead.</p>

<h2>Example 1: serif vs. sans-serif</h2>
<p><strong>Serif</strong> fonts (with small decorative strokes finishing
each letter) read as traditional, trustworthy, editorial — think
newspapers, novels, and academic publishing. <strong>Sans-serif</strong>
fonts (without those strokes, cleaner and more geometric) read as modern,
clean, digital-first — which is exactly why most app and website
interfaces default to a sans-serif typeface: it was designed for exactly
this reading context, on a screen, at typically smaller sizes.</p>

<h2>Example 2: pairing fonts without it looking accidental</h2>
<p>A reliable starting rule for beginners: pair no more than two
typefaces in one design, and make sure they contrast clearly in
<em>purpose</em> rather than just being slightly different — a bold serif
headline paired with a clean sans-serif body text reads as a deliberate
choice, while two fonts that are almost-but-not-quite the same just reads
as an accident, as if you meant to pick one font and somehow ended up
with two.</p>

<h2>Example 3: line height and letter spacing</h2>
<pre><code>Too tight:  lines almost touching, text feels cramped and hard to scan
Too loose:  lines feel disconnected from each other, hard to follow
Just right: about 1.4-1.6x the font size — comfortable to read at length</code></pre>
<p>Cramped line spacing is genuinely exhausting to read for more than a
sentence or two; spacing that's too generous makes lines feel
disconnected from each other, and a reader can lose their place jumping
back to the start of the next line. Type set well doesn't just look
nicer in a screenshot — it measurably changes how long a real reader is
willing to keep reading before giving up, which is exactly the kind of
practical, testable skill the full track spends real studio time on.</p>

<p>This lesson is a locked preview — the full track includes hands-on
typography exercises with real feedback, not just theory.</p>
""",
    },
    {
        "slug": "getting-started-with-figma",
        "title": "Getting Started with Figma",
        "order": 5,
        "is_free": False,
        "summary": "The industry-standard design tool most working designers use daily — frames, components, and designing with real limits in mind.",
        "body": """
<p>Figma is a browser-based design tool that's become the industry
standard for interface design — largely because it makes real-time
collaboration and clean handoff to developers dramatically easier than
the desktop-only design tools it mostly replaced.</p>

<h2>Example 1: frames, not an infinite canvas</h2>
<p>Instead of one infinite blank canvas, Figma organizes work into
<strong>frames</strong> — fixed-size containers that map directly onto a
real screen size (an iPhone, a desktop browser window). Designing inside
the actual target dimensions from the very start avoids a whole category
of "this looked perfect in the mockup, then broke the moment we saw it on
a real device" problems that plague designs built without real
constraints in mind.</p>

<h2>Example 2: components</h2>
<pre><code>Button component (defined once)
  -> used on the homepage
  -> used on the signup page
  -> used on the checkout page

Update the original component's color once
  -> all three places update automatically</code></pre>
<p>A <strong>component</strong> is a reusable element — a button, a
card, a navigation bar — defined exactly once and reused everywhere it
appears. Update the original, and every single place it's used across
the whole file updates automatically, instantly. This is the exact same
underlying idea as a reusable code component (which you'll meet again if
you ever cross into the Frontend track), and it's what makes a real
design system maintainable over months, instead of slowly turning into a
pile of one-off screens that quietly drift apart from each other.</p>

<h2>Why designing with real constraints beats designing freely</h2>
<p>Working designers design already knowing what a developer will
actually be able to build: consistent spacing values reused everywhere
rather than invented per-screen, real font sizes from an actual defined
scale, colors saved as reusable named styles rather than one-off picks
that are nearly impossible to update consistently later. This is exactly
where design work starts to directly connect with the Frontend track's
CSS lessons, and it's exactly the kind of practical, portfolio-ready
skill the full track builds hands-on, not just as theory.</p>
""",
    },
]

TRACKS = {
    "frontend": FRONTEND_LESSONS,
    "backend": BACKEND_LESSONS,
    "cybersecurity": CYBERSECURITY_LESSONS,
    "graphic_design": GRAPHIC_DESIGN_LESSONS,
}


class Command(BaseCommand):
    help = (
        "Seeds original sample lessons for every cohort track — a free-preview "
        "funnel into paid enrollment. Written from scratch for this project, "
        "not copied from anywhere. Idempotent, safe to rerun."
    )

    def handle(self, *args, **options):
        for track_slug, lessons in TRACKS.items():
            try:
                track = Track.objects.get(slug=track_slug)
            except Track.DoesNotExist:
                raise CommandError(f"Run `python manage.py seed_data` first — the {track_slug} track doesn't exist yet.")

            for data in lessons:
                data = dict(data)
                slug = data.pop("slug")
                lesson, created = Lesson.objects.update_or_create(track=track, slug=slug, defaults=data)
                status = "created" if created else "updated"
                self.stdout.write(f"[{track_slug}] Lesson '{lesson.title}' {status}")

        self.stdout.write(self.style.SUCCESS("Sample lessons ready for every track."))
