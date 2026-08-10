from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to CSS",
        "slug": "introduction",
        "order": 1,
        "summary": "What CSS is, and the three ways to attach it to an HTML page.",
        "body": """
<p>CSS (Cascading Style Sheets) controls how HTML looks: colors, spacing, fonts, layout.
HTML says <em>what</em> something is; CSS says how it should <em>appear</em>.</p>
<p>A CSS rule has a <strong>selector</strong> (what to style) and a block of
<strong>declarations</strong> (property: value pairs) in curly braces. You can write CSS
inline on a tag, in a <code>&lt;style&gt;</code> block in the page's head, or in a separate
<code>.css</code> file linked with <code>&lt;link&gt;</code> &mdash; a separate file is the
usual choice for real projects, since it keeps styling out of your markup.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  h1 { color: #2f7dff; }
  p { color: #444; font-size: 18px; }
</style>
</head>
<body>

  <h1>Styled Heading</h1>
  <p>This paragraph is styled by the CSS rules above.</p>

</body>
</html>
""",
    },
    {
        "title": "Selectors",
        "slug": "selectors",
        "order": 2,
        "summary": "Targeting elements by tag, class, id, or combinations of these.",
        "body": """
<p>A <strong>tag selector</strong> (<code>p</code>) styles every element of that type.
A <strong>class selector</strong> (<code>.highlight</code>) styles every element with
<code>class="highlight"</code>. An <strong>id selector</strong> (<code>#header</code>)
targets the one element with that id. You can combine them &mdash;
<code>p.highlight</code> only matches paragraphs that also have the highlight class.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  p { font-family: sans-serif; }
  .highlight { background: yellow; }
  #special { color: red; font-weight: bold; }
</style>
</head>
<body>

  <p class="highlight">Every paragraph gets sans-serif; this one is also highlighted.</p>
  <p id="special">This paragraph is targeted by its id.</p>

</body>
</html>
""",
    },
    {
        "title": "Colors & Backgrounds",
        "slug": "colors-and-backgrounds",
        "order": 3,
        "summary": "Setting text color and background color, by name, hex, or rgb.",
        "body": """
<p><code>color</code> sets text color; <code>background-color</code> sets the background.
Both accept a named color (<code>red</code>), a hex code (<code>#ff5733</code>), or an
<code>rgb()</code>/<code>rgba()</code> value (the last number in <code>rgba</code> controls
opacity, from 0 to 1).</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  body { background-color: #0d1224; }
  h1 { color: white; }
  p { color: rgba(255, 255, 255, 0.8); background-color: rgba(47, 125, 255, 0.2); padding: 10px; }
</style>
</head>
<body>

  <h1>Dark Themed Page</h1>
  <p>Semi-transparent text on a semi-transparent background box.</p>

</body>
</html>
""",
    },
    {
        "title": "The Box Model",
        "slug": "box-model",
        "order": 4,
        "summary": "Content, padding, border, and margin — every element is a box.",
        "body": """
<p>Every HTML element is a rectangular box made of four layers, from the inside out:
<strong>content</strong> (the text/image itself), <strong>padding</strong> (space inside
the border), <strong>border</strong> (a visible line around the padding), and
<strong>margin</strong> (space outside the border, between this box and its neighbours).
Understanding this layering explains almost every spacing question you'll ever have in CSS.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .box {
    width: 200px;
    padding: 20px;
    border: 4px solid #2f7dff;
    margin: 30px;
    background: #eef4ff;
  }
</style>
</head>
<body>

  <div class="box">Content sits inside the padding, which sits inside the border.</div>

</body>
</html>
""",
    },
    {
        "title": "Text & Fonts",
        "slug": "text-and-fonts",
        "order": 5,
        "summary": "font-family, font-size, font-weight, and text-align.",
        "body": """
<p><code>font-family</code> picks the typeface (list a few, ending in a generic fallback
like <code>sans-serif</code>, in case the first choice isn't installed).
<code>font-size</code> controls how big the text is, <code>font-weight</code> controls
boldness (<code>normal</code>, <code>bold</code>, or a number like <code>600</code>), and
<code>text-align</code> controls horizontal alignment (<code>left</code>,
<code>center</code>, <code>right</code>).</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  h1 { font-family: Georgia, serif; text-align: center; }
  p { font-family: Arial, sans-serif; font-size: 16px; font-weight: 600; text-align: justify; }
</style>
</head>
<body>

  <h1>A Serif Heading, Centered</h1>
  <p>A bolder, sans-serif paragraph, justified so both edges line up evenly across the page.</p>

</body>
</html>
""",
    },
    {
        "title": "Flexbox",
        "slug": "flexbox",
        "order": 6,
        "summary": "Laying out a row (or column) of items with display: flex.",
        "body": """
<p>Setting <code>display: flex</code> on a container turns its direct children into a
flexible row by default. <code>justify-content</code> controls spacing along that row
(<code>space-between</code>, <code>center</code>, ...), and <code>align-items</code>
controls vertical alignment within the row. Flexbox is the go-to tool for things like
navigation bars and card rows.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0d1224;
    padding: 12px 20px;
  }
  .nav a { color: white; text-decoration: none; margin-left: 16px; }
</style>
</head>
<body>

  <div class="nav">
    <strong style="color:white;">Logo</strong>
    <div>
      <a href="#">Home</a>
      <a href="#">About</a>
      <a href="#">Contact</a>
    </div>
  </div>

</body>
</html>
""",
    },
    {
        "title": "Grid",
        "slug": "grid",
        "order": 7,
        "summary": "Two-dimensional layouts with display: grid.",
        "body": """
<p>While flexbox is great for one row (or one column), <code>display: grid</code> lays
things out in rows <em>and</em> columns at once. <code>grid-template-columns</code>
defines how many columns and how wide each is; <code>gap</code> adds space between cells.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .gallery {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
  }
  .gallery div {
    background: #2f7dff;
    color: white;
    padding: 30px;
    text-align: center;
    border-radius: 8px;
  }
</style>
</head>
<body>

  <div class="gallery">
    <div>1</div>
    <div>2</div>
    <div>3</div>
    <div>4</div>
    <div>5</div>
    <div>6</div>
  </div>

</body>
</html>
""",
    },
    {
        "title": "Positioning",
        "slug": "positioning",
        "order": 8,
        "summary": "static, relative, absolute, and fixed positioning.",
        "body": """
<p>By default, elements are <code>position: static</code> &mdash; they flow normally on
the page. <code>relative</code> nudges an element from where it would normally sit, without
affecting other elements. <code>absolute</code> removes it from normal flow entirely and
positions it relative to its nearest positioned ancestor. <code>fixed</code> positions it
relative to the browser window, so it stays put even when the page scrolls.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .card { position: relative; border: 1px solid #ccc; padding: 20px; margin: 40px; }
  .badge {
    position: absolute;
    top: -10px;
    right: -10px;
    background: red;
    color: white;
    padding: 4px 8px;
    border-radius: 999px;
    font-size: 12px;
  }
</style>
</head>
<body>

  <div class="card">
    A card with a badge positioned relative to it.
    <span class="badge">New</span>
  </div>

</body>
</html>
""",
    },
    {
        "title": "Responsive Design (Media Queries)",
        "slug": "media-queries",
        "order": 9,
        "summary": "Changing styles based on screen width with @media.",
        "body": """
<p>A <code>@media</code> rule applies its styles only when a condition is met &mdash; most
often a screen width. This is how a page rearranges itself for phones vs. desktops: write
your default (usually mobile) styles first, then override them inside a
<code>@media (min-width: ...)</code> block for larger screens.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  .box { background: #2f7dff; color: white; padding: 20px; }
  @media (min-width: 500px) {
    .box { background: #ff7a2f; }
  }
</style>
</head>
<body>

  <div class="box">Resize your browser (or this preview) past 500px wide to see the color change.</div>

</body>
</html>
""",
    },
    {
        "title": "Transitions & Hover Effects",
        "slug": "transitions",
        "order": 10,
        "summary": "Animating property changes smoothly with the transition property.",
        "body": """
<p><code>transition</code> tells the browser to animate a property change instead of
jumping instantly. Pair it with <code>:hover</code> (a pseudo-class matching an element
while the mouse is over it) for smooth interactive effects &mdash; a very common pattern for
buttons and cards.</p>
""",
        "example_code": """<!DOCTYPE html>
<html>
<head>
<style>
  button {
    background: #2f7dff;
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.3s ease;
  }
  button:hover {
    background: #1f5fe0;
    transform: translateY(-3px);
  }
</style>
</head>
<body>

  <button>Hover over me</button>

</body>
</html>
""",
    },
]


def seed_css_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject, _ = Subject.objects.update_or_create(
        slug="css",
        defaults={
            "name": "CSS",
            "icon": "\U0001F3A8",
            "description": "The language for styling and laying out HTML pages.",
            "editor_language": "css",
            "order": 2,
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


def unseed_css_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="css").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0003_alter_subject_editor_language"),
    ]

    operations = [
        migrations.RunPython(seed_css_subject, unseed_css_subject),
    ]
