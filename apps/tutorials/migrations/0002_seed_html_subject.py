from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to HTML",
        "slug": "introduction",
        "order": 1,
        "summary": "What HTML is, and the basic structure every HTML page shares.",
        "body": """
<p>HTML (HyperText Markup Language) is the language browsers use to understand what's on a
web page: which text is a heading, which is a paragraph, where an image goes, where a link
points to. It doesn't make a page pretty on its own &mdash; that's CSS's job &mdash; it just
describes the page's structure and content.</p>
<p>Every HTML document follows the same basic skeleton. Edit the example below and press
Run to see it change instantly.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
  <title>My First Page</title>
</head>
<body>

  <h1>Hello, world!</h1>
  <p>This is a paragraph of text on my very first HTML page.</p>

</body>
</html>
""",
    },
    {
        "title": "Elements, Tags & Attributes",
        "slug": "elements-and-attributes",
        "order": 2,
        "summary": "How tags wrap content to form elements, and how attributes add extra detail.",
        "body": """
<p>Most HTML <strong>elements</strong> have an opening tag, some content, and a closing tag:
<code>&lt;p&gt;content&lt;/p&gt;</code>. A few elements, like <code>&lt;img&gt;</code> and
<code>&lt;br&gt;</code>, don't wrap anything and don't need a closing tag.</p>
<p><strong>Attributes</strong> live inside the opening tag and give the browser extra
information about that element &mdash; a link's destination, an image's source, and so on.
They're written as <code>name="value"</code> pairs.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p title="This is a tooltip">Hover over this paragraph to see its title attribute.</p>
  <p>Elements can nest inside each other: <strong>this text is bold</strong> inside a paragraph.</p>

</body>
</html>
""",
    },
    {
        "title": "Headings & Paragraphs",
        "slug": "headings-and-paragraphs",
        "order": 3,
        "summary": "Structuring text with h1-h6 headings and the paragraph tag.",
        "body": """
<p>HTML gives you six levels of heading, <code>&lt;h1&gt;</code> through <code>&lt;h6&gt;</code>,
from most to least important. Use <code>&lt;h1&gt;</code> once per page for the main title, and
work down from there &mdash; don't skip levels just to make text bigger, that's what CSS is for.</p>
<p>Regular text goes in <code>&lt;p&gt;</code> paragraph tags. The browser automatically adds
space above and below each one.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <h1>Main Page Title</h1>
  <h2>A Section Heading</h2>
  <p>This is the first paragraph, explaining the section above.</p>
  <h2>Another Section</h2>
  <p>And another paragraph here.</p>

</body>
</html>
""",
    },
    {
        "title": "Text Formatting",
        "slug": "text-formatting",
        "order": 4,
        "summary": "Bold, italic, line breaks, and horizontal rules.",
        "body": """
<p>A few inline tags change how text looks: <code>&lt;strong&gt;</code> makes text bold
and signals it's important, <code>&lt;em&gt;</code> italicises text for emphasis.
<code>&lt;br&gt;</code> forces a line break without starting a new paragraph, and
<code>&lt;hr&gt;</code> draws a horizontal divider line.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p>This word is <strong>very important</strong>, and this one is <em>emphasised</em>.</p>
  <p>First line.<br>Second line, same paragraph.</p>
  <hr>
  <p>Text after the divider.</p>

</body>
</html>
""",
    },
    {
        "title": "Links",
        "slug": "links",
        "order": 5,
        "summary": "Connecting pages together with the anchor tag.",
        "body": """
<p>The <code>&lt;a&gt;</code> (anchor) tag creates a clickable link. The
<code>href</code> attribute sets where it points &mdash; another page, another site, or even
a spot further down the same page. Add <code>target="_blank"</code> to open the link in a new
tab.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <p><a href="https://www.mozilla.org/en-US/">Visit MDN Web Docs</a></p>
  <p><a href="https://www.mozilla.org/en-US/" target="_blank">Open it in a new tab instead</a></p>

</body>
</html>
""",
    },
    {
        "title": "Images",
        "slug": "images",
        "order": 6,
        "summary": "Embedding pictures with the img tag, and why alt text matters.",
        "body": """
<p>The <code>&lt;img&gt;</code> tag embeds a picture. It's self-closing &mdash; no separate
closing tag &mdash; and needs a <code>src</code> attribute pointing at the image file or URL.</p>
<p>Always add an <code>alt</code> attribute too: a short text description shown if the image
fails to load, and read aloud by screen readers for visually impaired visitors.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <img src="https://picsum.photos/seed/htmltutorial/400/200" alt="A random placeholder photo" width="400">

</body>
</html>
""",
    },
    {
        "title": "Lists",
        "slug": "lists",
        "order": 7,
        "summary": "Bulleted lists, numbered lists, and list items.",
        "body": """
<p>Use <code>&lt;ul&gt;</code> for an unordered (bulleted) list, or <code>&lt;ol&gt;</code>
for an ordered (numbered) list. Either way, each item goes inside its own
<code>&lt;li&gt;</code> tag.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <h3>Shopping list</h3>
  <ul>
    <li>Rice</li>
    <li>Tomatoes</li>
    <li>Pepper</li>
  </ul>

  <h3>Steps to make jollof rice</h3>
  <ol>
    <li>Blend the pepper and tomatoes</li>
    <li>Fry the base</li>
    <li>Add rice and stock, simmer</li>
  </ol>

</body>
</html>
""",
    },
    {
        "title": "Tables",
        "slug": "tables",
        "order": 8,
        "summary": "Rows, columns, and headers for tabular data.",
        "body": """
<p>A <code>&lt;table&gt;</code> is built from rows (<code>&lt;tr&gt;</code>), and each row
holds cells &mdash; either regular data cells (<code>&lt;td&gt;</code>) or header cells
(<code>&lt;th&gt;</code>), which browsers usually bold and centre automatically.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <table border="1" cellpadding="6">
    <tr>
      <th>Name</th>
      <th>Track</th>
    </tr>
    <tr>
      <td>Ada</td>
      <td>Frontend</td>
    </tr>
    <tr>
      <td>Chidi</td>
      <td>Cybersecurity</td>
    </tr>
  </table>

</body>
</html>
""",
    },
    {
        "title": "Forms",
        "slug": "forms",
        "order": 9,
        "summary": "Collecting input from visitors with form, input, label, and button.",
        "body": """
<p>The <code>&lt;form&gt;</code> tag wraps a group of input controls. A text field is an
<code>&lt;input type="text"&gt;</code>; pair each one with a <code>&lt;label&gt;</code> so
screen readers (and mouse clicks) know what it's for. A <code>&lt;button&gt;</code>
submits the form.</p>
<p>This example only demonstrates the markup &mdash; it isn't wired up to actually send
anywhere.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <form>
    <label for="name">Your name:</label><br>
    <input type="text" id="name" name="name"><br><br>

    <label for="track">Favourite track:</label><br>
    <select id="track" name="track">
      <option>Frontend</option>
      <option>Backend</option>
      <option>Cybersecurity</option>
    </select><br><br>

    <button type="submit">Submit</button>
  </form>

</body>
</html>
""",
    },
    {
        "title": "Div, Classes & Id",
        "slug": "div-classes-and-id",
        "order": 10,
        "summary": "Grouping content with div, and naming elements with class and id.",
        "body": """
<p><code>&lt;div&gt;</code> is a generic container with no meaning of its own &mdash; it just
groups other elements together so you can style or position them as a block.</p>
<p>The <code>class</code> attribute labels an element so CSS (or JavaScript) can target every
element sharing that label. <code>id</code> does the same thing but must be unique on the
page &mdash; only one element can have a given id.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .highlight { background: yellow; }
  #intro { font-style: italic; }
</style>
</head>
<body>

  <div id="intro">
    <p class="highlight">This paragraph has the "highlight" class.</p>
    <p>This one doesn't.</p>
  </div>

</body>
</html>
""",
    },
    {
        "title": "Semantic HTML",
        "slug": "semantic-html",
        "order": 11,
        "summary": "Tags that describe meaning, not just layout: header, nav, main, article, footer.",
        "body": """
<p>Instead of building every page out of nameless <code>&lt;div&gt;</code>s, HTML offers
tags that describe what a section <em>is</em>: <code>&lt;header&gt;</code> for the top of a
page, <code>&lt;nav&gt;</code> for navigation links, <code>&lt;main&gt;</code> for the primary
content, <code>&lt;article&gt;</code> for a self-contained piece of content, and
<code>&lt;footer&gt;</code> for the bottom. They behave like <code>&lt;div&gt;</code>
visually, but they help screen readers, search engines, and other developers understand
your page's structure at a glance.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<body>

  <header>
    <h1>My Blog</h1>
    <nav><a href="#">Home</a> | <a href="#">About</a></nav>
  </header>

  <main>
    <article>
      <h2>My First Post</h2>
      <p>Semantic tags make this structure obvious even without reading the CSS.</p>
    </article>
  </main>

  <footer>
    <p>&copy; 2026 My Blog</p>
  </footer>

</body>
</html>
""",
    },
    {
        "title": "Build Your First Page",
        "slug": "build-your-first-page",
        "order": 12,
        "summary": "A capstone example combining everything from this tutorial into one page.",
        "body": """
<p>You've now met headings, paragraphs, links, images, lists, tables, forms, and semantic
tags. This last example combines several of them into one small page &mdash; edit it freely
and see what breaks (nothing will &mdash; it's a sandbox!).</p>
<p>From here, our tutors' full HTML/CSS course goes further: real layouts, styling every
element you just learned, and building complete responsive pages.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<title>My Portfolio</title>
</head>
<body>

  <header>
    <h1>Ada Okafor</h1>
    <p><em>Frontend developer in training</em></p>
  </header>

  <main>
    <h2>Projects</h2>
    <ul>
      <li><a href="#">To-do list app</a></li>
      <li><a href="#">Weather widget</a></li>
    </ul>

    <h2>Contact</h2>
    <form>
      <label for="email">Email me:</label>
      <input type="text" id="email" name="email">
      <button type="submit">Send</button>
    </form>
  </main>

  <footer>
    <p>&copy; 2026 Ada Okafor</p>
  </footer>

</body>
</html>
""",
    },
]


def seed_html_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="html",
        defaults={
            "name": "HTML",
            "icon": "\U0001F310",
            "description": "The standard markup language for structuring content on the web.",
            "editor_language": "html",
            "order": 1,
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
            },
        )


def unseed_html_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="html").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_html_subject, unseed_html_subject),
    ]
