from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "What HTML actually is, why it's not a programming language, and the basic structure every HTML page shares.",
        "body": """
<p>HTML (HyperText Markup Language) is the language browsers use to
understand what's on a web page: which text is a heading, which is a
paragraph, where an image goes, where a link points to. It is not a
programming language — it has no <code>if</code> statements, no math, no
way to make a decision. It's a <strong>markup language</strong>: a system
for wrapping content in tags that say what each piece <em>is</em>,
leaving the "how it looks" to CSS and the "how it behaves" to JavaScript.</p>

<p>Why does the split matter? Because it means three completely different
skills — structure, style, and behavior — can each be worked on
independently without breaking the others. Change a page's colors
entirely, and its HTML structure doesn't need to change at all.</p>

<h2>A little context: two more small examples first</h2>
<pre><code>&lt;h1&gt;Page Title&lt;/h1&gt;
&lt;p&gt;A short paragraph.&lt;/p&gt;
&lt;ul&gt;
  &lt;li&gt;First item&lt;/li&gt;
  &lt;li&gt;Second item&lt;/li&gt;
&lt;/ul&gt;</code></pre>
<p>Notice the repeating pattern: a tag names what something is
(<code>h1</code> = "main heading," <code>li</code> = "list item"), and
whatever sits inside it is the content that label applies to. That
pattern — a tag wrapping content — is nearly all of HTML.</p>

<p>Every HTML document also follows the same basic skeleton, shown in the
editable example below. Edit it and press Run to see your changes appear
instantly on the right — that live preview is exactly how you'll explore
every example in this tutorial.</p>
""",
    },
    {
        "slug": "elements-and-attributes",
        "summary": "How tags wrap content to form elements, how attributes add extra detail, and why the distinction between the two matters.",
        "body": """
<p>Most HTML <strong>elements</strong> have an opening tag, some content,
and a closing tag: <code>&lt;p&gt;content&lt;/p&gt;</code>. A few
elements, like <code>&lt;img&gt;</code> and <code>&lt;br&gt;</code>,
don't wrap anything at all and don't need a closing tag — there's simply
nothing "inside" an image.</p>

<h2>Example 1: an attribute changing behavior</h2>
<pre><code>&lt;a href="https://example.com"&gt;Link&lt;/a&gt;
&lt;a href="https://example.com" target="_blank"&gt;Opens in a new tab&lt;/a&gt;</code></pre>
<p><strong>Attributes</strong> live inside the opening tag and give the
browser extra information about that specific element — here,
<code>target="_blank"</code> changes how the very same link behaves.
Attributes are written as <code>name="value"</code> pairs, and a single
tag can carry several at once.</p>

<h2>Example 2: nesting — elements inside elements</h2>
<pre><code>&lt;p&gt;This sentence has &lt;strong&gt;one important word&lt;/strong&gt; in it.&lt;/p&gt;</code></pre>
<p>Elements routinely nest inside each other: here, a
<code>&lt;strong&gt;</code> element sits entirely inside a
<code>&lt;p&gt;</code> element. The rule for valid nesting is simple but
important — whatever you open last, you must close first, like stacking
and unstacking boxes. <code>&lt;p&gt;&lt;strong&gt;text&lt;/p&gt;&lt;/strong&gt;</code>
(closed in the wrong order) is invalid HTML, even though it might still
render something on screen — browsers are forgiving, but "the browser
didn't complain" isn't the same as "this is correct."</p>

<p>Try editing the attributes in the example below — add a
<code>title="..."</code> attribute to the paragraph and hover over it in
the preview to see what happens.</p>
""",
    },
    {
        "slug": "headings-and-paragraphs",
        "summary": "Structuring text with h1–h6 headings and the paragraph tag — and why hierarchy matters more than how big something looks.",
        "body": """
<p>HTML gives you six levels of heading, <code>&lt;h1&gt;</code> through
<code>&lt;h6&gt;</code>, from most important to least. A page should
normally have exactly <strong>one</strong> <code>&lt;h1&gt;</code> — its
main title — and work down from there, the same way a book has one title
and then chapters and subheadings underneath it.</p>

<h2>Example 1: correct hierarchy</h2>
<pre><code>&lt;h1&gt;Code Secure Academy&lt;/h1&gt;
&lt;h2&gt;Our Tracks&lt;/h2&gt;
&lt;h3&gt;Frontend&lt;/h3&gt;
&lt;h3&gt;Backend&lt;/h3&gt;</code></pre>
<p>"Frontend" and "Backend" are both <code>&lt;h3&gt;</code> because
they're both subsections of "Our Tracks" — siblings at the same level get
the same heading level. Don't pick a heading level by how big you want
text to look on screen; that's what CSS is for. Heading levels exist to
describe real structure, which is what lets a screen reader user jump
directly between sections and what lets a search engine understand how a
page is organized.</p>

<h2>Example 2: paragraphs</h2>
<pre><code>&lt;p&gt;This is the first paragraph, with its own topic.&lt;/p&gt;
&lt;p&gt;This is a second, separate paragraph.&lt;/p&gt;</code></pre>
<p>Regular text goes in <code>&lt;p&gt;</code> paragraph tags. The
browser automatically adds visual space above and below each one — resist
the temptation to fake that spacing with repeated <code>&lt;br&gt;</code>
tags instead of actually starting a new paragraph, since that throws away
the real structural meaning that these are two separate thoughts.</p>
""",
    },
    {
        "slug": "text-formatting",
        "summary": "Bold, italic, line breaks, and horizontal rules — and why strong/em mean something beyond just looking different.",
        "body": """
<p>A handful of inline tags change how text is presented, and each one
carries real meaning beyond its default appearance.</p>

<h2>Example 1: strong vs. em</h2>
<pre><code>&lt;p&gt;This word is &lt;strong&gt;critically important&lt;/strong&gt;.&lt;/p&gt;
&lt;p&gt;This word needs &lt;em&gt;emphasis&lt;/em&gt; when read aloud.&lt;/p&gt;</code></pre>
<p><code>&lt;strong&gt;</code> makes text bold and signals it's genuinely
important; <code>&lt;em&gt;</code> italicizes text for emphasis. Browsers
render them as bold/italic by default, but their real job is
<em>meaning</em>, not appearance — a screen reader actually changes tone
of voice for them. If you just want text to <em>look</em> bold with no
real emphasis intended (a stylistic choice, not meaning), that's a job
for CSS's <code>font-weight</code> property instead.</p>

<h2>Example 2: line breaks and dividers</h2>
<pre><code>&lt;p&gt;123 Main Street&lt;br&gt;Lagos, Nigeria&lt;/p&gt;
&lt;hr&gt;
&lt;p&gt;Text after the divider.&lt;/p&gt;</code></pre>
<p><code>&lt;br&gt;</code> forces a line break <em>within</em> the same
paragraph — useful for something like an address, where lines are related
but not separate ideas. <code>&lt;hr&gt;</code> draws a horizontal
divider line, typically used to mark a thematic break between sections of
content.</p>
""",
    },
    {
        "slug": "links",
        "summary": "Connecting pages together with the anchor tag — absolute vs. relative links, and the security detail most tutorials skip.",
        "body": """
<p>The <code>&lt;a&gt;</code> (anchor) tag creates a clickable link. The
<code>href</code> attribute sets where it points — another page, another
site, or a spot further down the same page.</p>

<h2>Example 1: absolute vs. relative links</h2>
<pre><code>&lt;a href="https://mozilla.org"&gt;Absolute — full address&lt;/a&gt;
&lt;a href="/about"&gt;Relative — this same site's /about page&lt;/a&gt;</code></pre>
<p>An <strong>absolute</strong> link is a complete address to somewhere
else on the internet. A <strong>relative</strong> link means "this same
site's page at this path" with no domain written out — this is what
you'd use for links within your own project, since it keeps working
unchanged no matter what domain the site eventually gets deployed to.</p>

<h2>Example 2: opening a link safely in a new tab</h2>
<pre><code>&lt;a href="https://mozilla.org" target="_blank" rel="noopener"&gt;
  Opens in a new tab, safely
&lt;/a&gt;</code></pre>
<p><code>target="_blank"</code> opens the link in a new tab. Always pair
it with <code>rel="noopener"</code> — without it, the page you linked to
gains a small amount of programmatic access back to your original tab, a
real (if narrow) security gap. It costs nothing to add and is worth
making a permanent habit.</p>
""",
    },
    {
        "slug": "images",
        "summary": "Embedding pictures with the img tag, and why alt text is functional, not decorative.",
        "body": """
<p>The <code>&lt;img&gt;</code> tag embeds a picture. It's self-closing —
no separate closing tag — and needs a <code>src</code> attribute pointing
at the image file or URL.</p>

<h2>Example 1: a complete, correct image tag</h2>
<pre><code>&lt;img src="https://picsum.photos/seed/htmltutorial/400/200"
     alt="A random placeholder photo"
     width="400"&gt;</code></pre>
<p>Always add an <code>alt</code> attribute: a text description shown if
the image fails to load, and read aloud by screen readers for visually
impaired visitors. It is not optional decoration — a missing or lazy
<code>alt=""</code> on a meaningful image is one of the most common
accessibility mistakes on the web, and one of the cheapest to fix.</p>

<h2>Example 2: when alt text should be deliberately empty</h2>
<pre><code>&lt;img src="decorative-swirl.png" alt=""&gt;</code></pre>
<p>Not every image carries information — a purely decorative flourish
should use <code>alt=""</code> (present, but empty on purpose) so a
screen reader skips it silently instead of announcing something useless
like "decorative swirl image." Rule of thumb: if removing the image loses
information, describe it; if it loses nothing, mark it decorative.</p>
""",
    },
    {
        "slug": "lists",
        "summary": "Bulleted lists, numbered lists, and list items — and when to reach for which one.",
        "body": """
<p>Use <code>&lt;ul&gt;</code> for an unordered (bulleted) list, or
<code>&lt;ol&gt;</code> for an ordered (numbered) list. Either way, each
item goes inside its own <code>&lt;li&gt;</code> tag.</p>

<h2>Example 1: unordered — order doesn't matter</h2>
<pre><code>&lt;h3&gt;Shopping list&lt;/h3&gt;
&lt;ul&gt;
  &lt;li&gt;Rice&lt;/li&gt;
  &lt;li&gt;Tomatoes&lt;/li&gt;
  &lt;li&gt;Pepper&lt;/li&gt;
&lt;/ul&gt;</code></pre>
<p>Use <code>&lt;ul&gt;</code> whenever the sequence of items doesn't
actually matter — a shopping list reads the same regardless of which
order the items are written in.</p>

<h2>Example 2: ordered — sequence matters</h2>
<pre><code>&lt;h3&gt;Steps to make jollof rice&lt;/h3&gt;
&lt;ol&gt;
  &lt;li&gt;Blend the pepper and tomatoes&lt;/li&gt;
  &lt;li&gt;Fry the base&lt;/li&gt;
  &lt;li&gt;Add rice and stock, simmer&lt;/li&gt;
&lt;/ol&gt;</code></pre>
<p>Use <code>&lt;ol&gt;</code> whenever the sequence genuinely matters —
here, swapping steps 1 and 3 would actually break the recipe. That's the
whole test for choosing between the two: does the order carry meaning?</p>
""",
    },
    {
        "slug": "tables",
        "summary": "Rows, columns, and headers for tabular data — and why tables shouldn't be used for page layout.",
        "body": """
<p>A <code>&lt;table&gt;</code> is built from rows (<code>&lt;tr&gt;</code>),
and each row holds cells — either regular data cells
(<code>&lt;td&gt;</code>) or header cells (<code>&lt;th&gt;</code>),
which browsers usually bold and center automatically.</p>

<h2>Example: a simple data table</h2>
<pre><code>&lt;table border="1" cellpadding="6"&gt;
  &lt;tr&gt;
    &lt;th&gt;Name&lt;/th&gt;
    &lt;th&gt;Track&lt;/th&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Ada&lt;/td&gt;
    &lt;td&gt;Frontend&lt;/td&gt;
  &lt;/tr&gt;
  &lt;tr&gt;
    &lt;td&gt;Chidi&lt;/td&gt;
    &lt;td&gt;Cybersecurity&lt;/td&gt;
  &lt;/tr&gt;
&lt;/table&gt;</code></pre>
<p>The first row uses <code>&lt;th&gt;</code> for column headers; every
row after it uses <code>&lt;td&gt;</code> for the actual data. Screen
readers use these header cells to announce which column a value belongs
to as they read across a row — a real, functional reason to use
<code>&lt;th&gt;</code> correctly, not just for the bold styling.</p>

<p>One firm rule worth knowing early: tables are for tabular
<em>data</em> — things that genuinely have rows and columns, like a
schedule or a price list. Using a table to lay out an entire page
(sidebar in one cell, content in another) was common in the 1990s and is
considered broken practice today — that's what CSS layout tools like
Flexbox and Grid exist for.</p>
""",
    },
    {
        "slug": "forms",
        "summary": "Collecting input from visitors with form, input, label, and button — and the details that separate a usable form from a broken one.",
        "body": """
<p>The <code>&lt;form&gt;</code> tag wraps a group of input controls. A
text field is an <code>&lt;input type="text"&gt;</code>; pair each one
with a <code>&lt;label&gt;</code> so screen readers — and simple mouse
clicks — know what it's for.</p>

<h2>Example 1: a labelled text field</h2>
<pre><code>&lt;label for="name"&gt;Your name:&lt;/label&gt;
&lt;input type="text" id="name" name="name"&gt;</code></pre>
<p>The <code>for="name"</code> on the label connects it to the input
sharing that exact <code>id</code>. Clicking the label text focuses the
input, and a screen reader announces the label when the field is reached
— placeholder text alone can't do either of these things reliably.</p>

<h2>Example 2: choosing from options, and submitting</h2>
<pre><code>&lt;label for="track"&gt;Favourite track:&lt;/label&gt;
&lt;select id="track" name="track"&gt;
  &lt;option&gt;Frontend&lt;/option&gt;
  &lt;option&gt;Backend&lt;/option&gt;
  &lt;option&gt;Cybersecurity&lt;/option&gt;
&lt;/select&gt;

&lt;button type="submit"&gt;Submit&lt;/button&gt;</code></pre>
<p><code>&lt;select&gt;</code> gives a dropdown of fixed choices, useful
whenever the answer must be one of a known set rather than free text.
This example only demonstrates the markup — it isn't wired up to
actually send anywhere, since that's a backend's job, covered in a
different track entirely.</p>
""",
    },
    {
        "slug": "div-classes-and-id",
        "summary": "Grouping content with div, and naming elements with class and id — including why one of them must be unique and the other must not.",
        "body": """
<p><code>&lt;div&gt;</code> is a generic container with no meaning of its
own — it just groups other elements together so you can style or position
them as one block. It's one of the most-used tags in HTML precisely
because it's so unopinionated.</p>

<h2>Example: class vs. id, side by side</h2>
<pre><code>&lt;div id="intro"&gt;
  &lt;p class="highlight"&gt;This paragraph has the "highlight" class.&lt;/p&gt;
  &lt;p class="highlight"&gt;So does this one.&lt;/p&gt;
  &lt;p&gt;This one doesn't.&lt;/p&gt;
&lt;/div&gt;</code></pre>
<p>The <code>class</code> attribute labels an element so CSS (or
JavaScript) can target <em>every</em> element sharing that label at once
— here, both highlighted paragraphs share <code>class="highlight"</code>,
so one CSS rule styles them both identically. <code>id</code> does a
similar job, but with one crucial difference: an <code>id</code> must be
unique on the entire page — only one element is ever allowed to have a
given <code>id</code>, which is exactly why it's used above on the
containing <code>div</code>, the one specific section being referenced.</p>

<p>A useful rule of thumb: reach for <code>class</code> when several
elements should share the same styling, and reach for <code>id</code>
only when you need to refer to one specific, singular element — a page's
main navigation bar, for instance, but not a repeated card in a list of
many identical cards.</p>
""",
    },
    {
        "slug": "semantic-html",
        "summary": "Tags that describe meaning, not just layout — header, nav, main, article, footer — and why they beat a page built entirely from divs.",
        "body": """
<p>Instead of building every page out of nameless <code>&lt;div&gt;</code>s,
HTML offers tags that describe what a section of a page actually
<em>is</em>.</p>

<h2>Example: a page built from semantic tags</h2>
<pre><code>&lt;header&gt;
  &lt;h1&gt;My Blog&lt;/h1&gt;
  &lt;nav&gt;&lt;a href="#"&gt;Home&lt;/a&gt; | &lt;a href="#"&gt;About&lt;/a&gt;&lt;/nav&gt;
&lt;/header&gt;

&lt;main&gt;
  &lt;article&gt;
    &lt;h2&gt;My First Post&lt;/h2&gt;
    &lt;p&gt;Semantic tags make this structure obvious without reading any CSS.&lt;/p&gt;
  &lt;/article&gt;
&lt;/main&gt;

&lt;footer&gt;
  &lt;p&gt;&amp;copy; 2026 My Blog&lt;/p&gt;
&lt;/footer&gt;</code></pre>
<p><code>&lt;header&gt;</code> marks the top of a page,
<code>&lt;nav&gt;</code> marks navigation links, <code>&lt;main&gt;</code>
marks the primary content (there should only be one per page),
<code>&lt;article&gt;</code> marks a self-contained piece of content, and
<code>&lt;footer&gt;</code> marks the bottom. Visually, these behave
almost identically to a plain <code>&lt;div&gt;</code> — but semantically
they help screen readers jump directly to "the main content" or "the
navigation" the same way sighted users visually scan a page for those
same landmarks, and they help search engines understand a page's real
structure instead of guessing from a wall of identical <code>div</code>s.</p>
""",
    },
    {
        "slug": "build-your-first-page",
        "summary": "A capstone example combining headings, links, images, lists, forms, and semantic tags into one real page.",
        "body": """
<p>You've now met headings, paragraphs, links, images, lists, tables,
forms, and semantic tags. This capstone example combines several of them
into one small, realistic page — a personal portfolio — so you can see
how they actually work together rather than in isolation.</p>

<h2>What to notice as you read this</h2>
<p>The page uses exactly one <code>&lt;h1&gt;</code> (the name), semantic
<code>&lt;header&gt;</code>/<code>&lt;main&gt;</code>/<code>&lt;footer&gt;</code>
sections instead of unlabeled <code>&lt;div&gt;</code>s, a real
<code>&lt;ul&gt;</code> for the project list since order doesn't matter
there, and a labelled form input rather than bare placeholder text. Every
choice traces back to a lesson you've already read — that's deliberate:
real pages are built by combining a small number of well-understood
pieces, not by learning some separate "how to build a whole page" trick.</p>

<p>Edit the example freely and see what breaks — nothing will, it's a
sandbox. From here, our tutors' full HTML/CSS course goes further: real
layouts, styling every element you've just learned, and building
complete, responsive pages.</p>
""",
    },
]


def deepen_html_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="html")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0027_seed_swift_subject"),
    ]

    operations = [
        migrations.RunPython(deepen_html_content, noop),
    ]
