from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "What CSS is, how a rule is structured, and the three ways to attach it — with why one of them is almost always the right choice.",
        "body": """
<p>CSS (Cascading Style Sheets) controls how HTML looks: colors, spacing,
fonts, layout. HTML says <em>what</em> something is; CSS says how it
should <em>appear</em>. Keeping those two jobs separate is what lets you
completely redesign a page's look without touching its structure at all.</p>

<h2>Example 1: the anatomy of a rule</h2>
<pre><code>h1 {
  color: #2f7dff;
  font-size: 32px;
}</code></pre>
<p>A CSS rule has a <strong>selector</strong> (<code>h1</code> — what to
style) and a block of <strong>declarations</strong> in curly braces, each
a <code>property: value;</code> pair. This one rule applies to every
<code>&lt;h1&gt;</code> on the page at once.</p>

<h2>Example 2: three ways to attach CSS, and why one wins</h2>
<pre><code>&lt;!-- 1. Inline — on one element, avoid this --&gt;
&lt;p style="color: red;"&gt;Text&lt;/p&gt;

&lt;!-- 2. Internal — in the page's head --&gt;
&lt;style&gt; p { color: red; } &lt;/style&gt;

&lt;!-- 3. External — a separate .css file, the usual real-project choice --&gt;
&lt;link rel="stylesheet" href="styles.css"&gt;</code></pre>
<p>An external file is almost always the right choice for a real project:
one file can style every page on a whole site, the browser caches it so
repeat visits load faster, and it keeps styling completely out of your
HTML markup, exactly matching the "what vs. how it looks" split this
lesson opened with.</p>
""",
    },
    {
        "slug": "selectors",
        "summary": "Targeting elements by tag, class, id, or combinations of these — and how CSS decides which rule wins when two rules conflict.",
        "body": """
<p>A <strong>tag selector</strong> (<code>p</code>) styles every element
of that type. A <strong>class selector</strong> (<code>.highlight</code>)
styles every element carrying <code>class="highlight"</code>. An
<strong>id selector</strong> (<code>#header</code>) targets the one
single element with that id.</p>

<h2>Example 1: combining selectors</h2>
<pre><code>p { font-family: sans-serif; }
.highlight { background: yellow; }
p.highlight { font-weight: bold; }</code></pre>
<p><code>p.highlight</code> (no space between them) only matches
paragraphs that <em>also</em> carry the highlight class — combining
selectors narrows what they match, while spacing them out
(<code>p .highlight</code>) would mean something different entirely: any
highlighted element <em>inside</em> a paragraph.</p>

<h2>Example 2: what happens when two rules disagree</h2>
<pre><code>p { color: blue; }
.highlight { color: red; }
/* A <p class="highlight"> ends up red — class beats tag selector */</code></pre>
<p>When two rules target the same element with different values for the
same property, CSS uses <strong>specificity</strong> to decide the
winner: id selectors beat class selectors, which beat tag selectors. This
is exactly why unexpected styling sometimes "just doesn't apply" — a more
specific rule elsewhere is quietly winning, and learning to check
specificity is often the fastest way to debug it.</p>
""",
    },
    {
        "slug": "colors-and-backgrounds",
        "summary": "Setting text and background color by name, hex, or rgb — and what that fourth rgba number actually controls.",
        "body": """
<p><code>color</code> sets text color; <code>background-color</code> sets
the background. Both accept a named color (<code>red</code>), a hex code
(<code>#ff5733</code>), or an <code>rgb()</code>/<code>rgba()</code>
value.</p>

<h2>Example 1: three ways to write the same color</h2>
<pre><code>h1 { color: red; }
h1 { color: #ff0000; }
h1 { color: rgb(255, 0, 0); }</code></pre>
<p>All three produce an identical red. Named colors are the most
readable for a handful of common colors; hex and <code>rgb()</code> let
you specify any of millions of exact shades, which is what you'll use for
anything matching a real brand palette.</p>

<h2>Example 2: rgba and transparency</h2>
<pre><code>.overlay {
  background-color: rgba(0, 0, 0, 0.5);
}</code></pre>
<p><code>rgba()</code> adds a fourth number — <strong>alpha</strong>,
from 0 (fully transparent, invisible) to 1 (fully solid). This example
creates a semi-transparent black overlay that lets whatever's underneath
still show through at half strength — a common pattern for darkening a
background image just enough to keep text readable on top of it.</p>
""",
    },
    {
        "slug": "box-model",
        "summary": "Content, padding, border, and margin — the four layers every element is built from, and the one setting that changes how they're measured.",
        "body": """
<p>Every HTML element is a rectangular box made of four layers, from the
inside out: <strong>content</strong> (the text/image itself),
<strong>padding</strong> (space inside the border),
<strong>border</strong> (a visible line around the padding), and
<strong>margin</strong> (space outside the border, between this box and
its neighbours).</p>

<h2>Example 1: seeing all four layers at once</h2>
<pre><code>.box {
  width: 200px;
  padding: 20px;
  border: 4px solid #2f7dff;
  margin: 30px;
}</code></pre>
<p>This box's actual rendered width, by default, is <em>more</em> than
200px — the browser adds the padding and border on top of the content
width you set. That surprises almost every beginner at least once.</p>

<h2>Example 2: box-sizing fixes the confusing part</h2>
<pre><code>.box {
  box-sizing: border-box;
  width: 200px;
  padding: 20px;
  border: 4px solid #2f7dff;
  /* now the box is EXACTLY 200px wide, padding and border included */
}</code></pre>
<p><code>box-sizing: border-box</code> changes the rule so
<code>width</code> means the <em>total</em> width, padding and border
included, rather than just the content. This one line eliminates a huge
share of "why is this wider than I set it to be" confusion, which is why
many real projects set it globally with <code>* { box-sizing: border-box; }</code>
right at the top of their stylesheet.</p>
""",
    },
    {
        "slug": "text-and-fonts",
        "summary": "font-family, font-size, font-weight, and text-align — and why a font-family list always needs a fallback.",
        "body": """
<p><code>font-family</code> picks the typeface, <code>font-size</code>
controls how big the text is, <code>font-weight</code> controls boldness,
and <code>text-align</code> controls horizontal alignment.</p>

<h2>Example 1: a font stack with a fallback</h2>
<pre><code>h1 { font-family: Georgia, "Times New Roman", serif; }</code></pre>
<p>The browser tries each font left to right and uses the first one
actually installed on the visitor's device, falling back to the generic
<code>serif</code> at the end if neither named font is available. Always
end a font list with a generic fallback (<code>serif</code>,
<code>sans-serif</code>, or <code>monospace</code>) — without it, a
visitor missing every named font sees the browser's unpredictable default
instead of something in the style family you actually intended.</p>

<h2>Example 2: weight and alignment together</h2>
<pre><code>p {
  font-weight: 600;
  text-align: justify;
}</code></pre>
<p><code>font-weight</code> accepts keywords (<code>normal</code>,
<code>bold</code>) or a number from 100 (thin) to 900 (black) for finer
control when a typeface supports it. <code>text-align: justify</code>
stretches each line so both edges line up evenly — common in print, used
more sparingly on the web since it can create uneven gaps between words
on narrow columns.</p>
""",
    },
    {
        "slug": "flexbox",
        "summary": "Laying out a row (or column) of items with display: flex — the single most useful layout tool for everyday UI work.",
        "body": """
<p>Setting <code>display: flex</code> on a container turns its direct
children into a flexible row by default — arguably the single most
useful CSS layout tool for everyday interface work like navigation bars
and card rows.</p>

<h2>Example 1: a navigation bar, evenly spaced</h2>
<pre><code>.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}</code></pre>
<p><code>justify-content</code> controls spacing along the main row
direction — <code>space-between</code> pushes the first and last items to
the opposite edges with even gaps between everything in the middle.
<code>align-items: center</code> vertically centers everything in the
row, which alone eliminates a huge amount of the manual pixel-nudging
CSS layout used to require before flexbox existed.</p>

<h2>Example 2: flex-direction changes the axis entirely</h2>
<pre><code>.sidebar {
  display: flex;
  flex-direction: column;
  gap: 12px;
}</code></pre>
<p><code>flex-direction: column</code> stacks children vertically
instead of horizontally — <code>justify-content</code> and
<code>align-items</code> still work the same way, just along the new
axis. <code>gap</code> adds even spacing between items without needing
individual margins on each one, which is simpler to maintain since
there's exactly one value to change instead of margins on every child.</p>
""",
    },
    {
        "slug": "grid",
        "summary": "Two-dimensional layouts with display: grid — when to reach for it instead of flexbox.",
        "body": """
<p>While flexbox is great for laying out one row (or one column) at a
time, <code>display: grid</code> lays things out in rows <em>and</em>
columns at once — a genuinely two-dimensional layout tool.</p>

<h2>Example: a photo gallery grid</h2>
<pre><code>.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
}</code></pre>
<p><code>grid-template-columns: repeat(3, 1fr)</code> creates three equal
columns (<code>1fr</code> means "one fraction of the available space,"
so three of them split it evenly). Items simply flow into the grid left
to right, top to bottom, automatically wrapping to a new row once a row
fills up — you never manually decide which item goes on which row.</p>

<h2>Choosing between flexbox and grid</h2>
<p>A useful rule of thumb: reach for flexbox when you're arranging items
along a single line that may wrap (a row of tags, a nav bar), and reach
for grid when you're deliberately laying things out in both rows and
columns together (a photo gallery, a dashboard layout, a page's overall
structure). Many real interfaces use both at once — grid for the overall
page structure, flexbox inside individual grid cells.</p>
""",
    },
    {
        "slug": "positioning",
        "summary": "static, relative, absolute, and fixed positioning — and the parent/child relationship that makes absolute positioning predictable instead of confusing.",
        "body": """
<p>By default, every element is <code>position: static</code> — it flows
normally on the page, one after another. The other three values change
that in specific ways.</p>

<h2>Example 1: relative — nudging without disrupting anything else</h2>
<pre><code>.icon { position: relative; top: -3px; }</code></pre>
<p><code>relative</code> nudges an element from where it would normally
sit — here, 3px upward — <em>without</em> affecting where any other
element on the page ends up. It's often used just to make small visual
adjustments, like nudging an icon to align better with adjacent text.</p>

<h2>Example 2: absolute — positioned relative to its nearest positioned ancestor</h2>
<pre><code>.card { position: relative; }
.badge {
  position: absolute;
  top: -10px;
  right: -10px;
}</code></pre>
<p><code>absolute</code> removes an element from normal flow entirely and
positions it relative to its <strong>nearest ancestor that has any
position other than static</strong> — here, <code>.card</code>'s
<code>position: relative</code> makes it that anchor, so the badge sits
pinned to the card's corner no matter where the card itself moves on the
page. Forgetting to set <code>position: relative</code> on the parent is
one of the most common positioning bugs — without it, the absolute
element anchors to the entire page instead of the nearby card you meant.</p>

<h2>Example 3: fixed — anchored to the browser window</h2>
<pre><code>.back-to-top { position: fixed; bottom: 20px; right: 20px; }</code></pre>
<p><code>fixed</code> positions relative to the browser window itself,
so it stays in the same spot on screen even while the page scrolls —
exactly what you want for something like a persistent "back to top"
button.</p>
""",
    },
    {
        "slug": "media-queries",
        "summary": "Changing styles based on screen width with @media — and why the mobile-first approach beats designing desktop-first.",
        "body": """
<p>A <code>@media</code> rule applies its styles only when a condition is
met — most often a screen width. This is how a page rearranges itself
for phones vs. desktops.</p>

<h2>Example: mobile-first responsive styling</h2>
<pre><code>.box {
  background: #2f7dff; /* the default, for small screens */
  padding: 12px;
}

@media (min-width: 768px) {
  .box {
    background: #ff7a2f; /* overridden once the screen is wide enough */
    padding: 24px;
  }
}</code></pre>
<p>The common convention — used above — is <strong>mobile-first</strong>:
write your default styles for the smallest screen first, then use
<code>@media (min-width: ...)</code> to progressively add or override
styles as the screen gets wider. This tends to produce simpler CSS than
the reverse (desktop-first, using <code>max-width</code> to strip things
away), since you're always adding complexity as space allows rather than
trying to cram a complex desktop layout back down.</p>

<h2>Common breakpoints worth knowing, not memorizing exactly</h2>
<p>There's no single "correct" set of screen-width breakpoints — real
projects pick values based on where their own design actually starts
looking cramped, commonly somewhere near 480px (large phones), 768px
(tablets), and 1024px (small laptops). Treat these as a starting point to
test against, not a rule to follow blindly.</p>
""",
    },
    {
        "slug": "transitions",
        "summary": "Animating property changes smoothly with the transition property — and why it needs to be paired with :hover to actually be noticed.",
        "body": """
<p><code>transition</code> tells the browser to animate a property
change smoothly instead of jumping to the new value instantly. On its
own it does nothing visible — it needs something that actually
<em>changes</em> a property to animate, which is exactly what
<code>:hover</code> provides.</p>

<h2>Example: a button that responds to hovering</h2>
<pre><code>button {
  background: #2f7dff;
  transform: translateY(0);
  transition: background 0.3s ease, transform 0.3s ease;
}
button:hover {
  background: #1f5fe0;
  transform: translateY(-3px);
}</code></pre>
<p><code>:hover</code> is a <strong>pseudo-class</strong> — a selector
matching an element only while a specific condition is true (here, the
mouse is over it). The moment the mouse enters, the button's background
and vertical position both change; because <code>transition</code> is
set on the base <code>button</code> rule (not just the hover rule), the
browser smoothly animates <em>both</em> changes over 0.3 seconds instead
of snapping instantly, and smoothly reverses the same animation on mouse-out.</p>

<p>This is one of the cheapest ways to make an interface feel polished
and responsive — a plain instant color swap on hover works, but a short,
smooth transition is what actually reads as "considered" rather than
"functional."</p>
""",
    },
]


def deepen_css_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="css")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0028_deepen_html_content"),
    ]

    operations = [
        migrations.RunPython(deepen_css_content, noop),
    ]
