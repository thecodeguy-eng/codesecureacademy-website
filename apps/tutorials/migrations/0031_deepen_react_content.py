from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "A JavaScript library for building UIs out of reusable components — what problem it actually solves, compared to plain JavaScript DOM manipulation.",
        "body": """
<p>React is a JavaScript library for building user interfaces out of
small, reusable <strong>components</strong> — each one a JavaScript
function that returns what should appear on screen.</p>

<h2>The problem React actually solves</h2>
<p>In plain JavaScript, updating the page means manually finding an
element and changing it — <code>document.getElementById(...).textContent = ...</code>,
over and over, once per thing that can change. That gets genuinely hard
to manage once a page has dozens of interconnected pieces that all need
to stay in sync with each other. React flips the approach: instead of
manually updating specific elements, you describe what the UI
<em>should</em> look like for the current data, and React figures out
exactly which real DOM elements need to change to match — you stop
thinking about "how do I update this," and start thinking about "what
should this look like right now."</p>

<h2>Example: a minimal component</h2>
<pre><code>function App() {
  return &lt;h1&gt;Hello, world!&lt;/h1&gt;;
}</code></pre>
<p>React code is normally compiled by a build tool before it reaches the
browser, so these examples are shown read-only rather than
live-editable — but the code itself is exactly what you'd write and run
in a real React project.</p>
""",
    },
    {
        "slug": "jsx",
        "summary": "Writing HTML-like markup directly inside JavaScript — and why the curly braces are the part that actually matters.",
        "body": """
<p>JSX is the syntax that lets you write HTML-like markup inside a
JavaScript function. It isn't a string, and it isn't real HTML either —
it compiles down to regular JavaScript function calls that build up the
UI piece by piece.</p>

<h2>Example: mixing markup and real JavaScript</h2>
<pre><code>function Greeting() {
  const name = "Ada";
  const hour = 14;
  return (
    &lt;div&gt;
      &lt;p&gt;Hello, {name}!&lt;/p&gt;
      &lt;p&gt;2 + 2 is {2 + 2}.&lt;/p&gt;
      &lt;p&gt;{hour < 18 ? "Good afternoon" : "Good evening"}&lt;/p&gt;
    &lt;/div&gt;
  );
}</code></pre>
<p>Curly braces <code>{ }</code> are the escape hatch back into real
JavaScript — anything inside them is evaluated as an expression, not
printed as literal text. A variable, a calculation, even a ternary
expression like the third line above all work exactly the way they would
in ordinary JavaScript, just embedded directly inside markup. This is
JSX's whole value: markup and the logic that drives it live in the same
place, instead of split across a template file and a separate script.</p>
""",
    },
    {
        "slug": "components-and-props",
        "summary": "Passing data into a component from its parent — the mechanism that lets one component get reused with different data.",
        "body": """
<p>A component is just a function; <strong>props</strong> are the
arguments you pass it, written like HTML attributes.</p>

<h2>Example: the same component, reused with different data</h2>
<pre><code>function Greeting(props) {
  return &lt;p&gt;Hello, {props.name}! You're studying {props.track}.&lt;/p&gt;;
}

function App() {
  return (
    &lt;div&gt;
      &lt;Greeting name="Ada" track="Frontend" /&gt;
      &lt;Greeting name="Chidi" track="Cybersecurity" /&gt;
    &lt;/div&gt;
  );
}</code></pre>
<p>Inside the component, every prop you passed arrives bundled into a
single object — <code>props.name</code>, <code>props.track</code>. This
is exactly what makes one component definition reusable across an entire
app: <code>Greeting</code> is written once, but rendered twice above with
completely different data each time, the same way a function can be
called repeatedly with different arguments.</p>

<h2>A common shortcut: destructuring props</h2>
<pre><code>function Greeting({ name, track }) {
  return &lt;p&gt;Hello, {name}! You're studying {track}.&lt;/p&gt;;
}</code></pre>
<p>This is functionally identical to the version above — it just unpacks
<code>name</code> and <code>track</code> directly out of the props object
in the function's parameter list, which is common enough in real React
code that it's worth recognizing even before you're writing it yourself.</p>
""",
    },
    {
        "slug": "usestate",
        "summary": "Giving a component memory that persists between renders — the core mechanism behind any interactive React UI.",
        "body": """
<p><code>useState</code> gives a component a piece of data that persists
across re-renders, and a function to update it.</p>

<h2>Example: a counter, and why it actually updates on screen</h2>
<pre><code>import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    &lt;div&gt;
      &lt;p&gt;Count: {count}&lt;/p&gt;
      &lt;button onClick={() => setCount(count + 1)}&gt;Add&lt;/button&gt;
    &lt;/div&gt;
  );
}</code></pre>
<p><code>useState(0)</code> returns two things: the current value
(<code>count</code>, starting at 0) and a function to change it
(<code>setCount</code>). Calling <code>setCount(count + 1)</code> doesn't
just change a variable quietly in the background — it tells React
"something changed, please re-run this component and update the screen
to match." That re-run-and-redraw step is the entire mechanism behind
every interactive React UI, from a simple counter to a full form.</p>

<h2>Why you can't just reassign a normal variable instead</h2>
<pre><code>let count = 0;
count = count + 1; // this changes the variable, but the screen never updates</code></pre>
<p>A plain variable change is invisible to React — nothing tells it to
re-run the component. <code>useState</code>'s update function is what
actually connects a data change to a visible screen update; that
connection is the entire reason it exists instead of an ordinary
variable.</p>
""",
    },
    {
        "slug": "useeffect",
        "summary": "Running code in response to a component rendering or its data changing — and what that dependency array actually controls.",
        "body": """
<p><code>useEffect</code> runs code after a component renders — fetching
data, subscribing to something, or manually touching the DOM.</p>

<h2>Example: a live-updating clock</h2>
<pre><code>import { useState, useEffect } from "react";

function Clock() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(id);
  }, []);

  return &lt;p&gt;Current time: {time}&lt;/p&gt;;
}</code></pre>
<p>The second argument, <code>[]</code> — an empty
<strong>dependency array</strong> — tells React "only run this effect
once, right after the very first render," rather than after every single
re-render. Change it to <code>[time]</code> and the effect would instead
re-run every time <code>time</code> changes — usually not what you'd
want here, since it would reset the interval constantly instead of
letting it tick steadily.</p>

<h2>Why the function returned inside useEffect matters</h2>
<p>The function returned from the effect (<code>() => clearInterval(id)</code>)
is <strong>cleanup</strong> — React calls it automatically if the
component is removed from the page, stopping the interval so it doesn't
keep silently running (and wasting resources) after the clock is no
longer even visible. Forgetting cleanup for things like intervals,
timers, and subscriptions is a very common source of subtle bugs in real
React apps.</p>
""",
    },
    {
        "slug": "handling-events",
        "summary": "Responding to clicks, typing, and other user interaction — the camelCase event props that connect markup to logic.",
        "body": """
<p>React event handlers are camelCase props — <code>onClick</code>,
<code>onChange</code>, <code>onSubmit</code> — set to a function that
runs whenever that event fires.</p>

<h2>Example: reading what's typed into a field</h2>
<pre><code>import { useState } from "react";

function SearchBox() {
  const [query, setQuery] = useState("");

  function handleChange(e) {
    setQuery(e.target.value);
  }

  return (
    &lt;div&gt;
      &lt;input type="text" onChange={handleChange} placeholder="Search..." /&gt;
      &lt;p&gt;You typed: {query}&lt;/p&gt;
    &lt;/div&gt;
  );
}</code></pre>
<p><code>e</code> (the event object) is passed automatically to every
handler; <code>e.target</code> is the actual DOM element the event
happened on, and <code>.value</code> is its current text. Notice this
example pairs the event handler with <code>useState</code> from the
previous lesson — reading input and storing it in state together is
exactly the pattern behind essentially every form in a real React app.</p>
""",
    },
    {
        "slug": "conditional-rendering",
        "summary": "Showing different markup depending on a condition — three common patterns, and when to reach for each.",
        "body": """
<p>Since JSX is just JavaScript, you use normal JavaScript to decide what
to render — no special "if tag" exists in JSX itself.</p>

<h2>Example 1: a ternary for an either/or choice</h2>
<pre><code>function Status({ loggedIn }) {
  return &lt;p&gt;{loggedIn ? "Welcome back!" : "Please log in."}&lt;/p&gt;;
}</code></pre>
<p>A ternary (<code>condition ? a : b</code>) fits neatly inline inside
JSX, which is why it's the most common choice for a simple two-way
choice like this one.</p>

<h2>Example 2: && for "render this, or render nothing"</h2>
<pre><code>function Notification({ hasUnread }) {
  return (
    &lt;div&gt;
      &lt;p&gt;Inbox&lt;/p&gt;
      {hasUnread && &lt;span&gt;You have unread messages&lt;/span&gt;}
    &lt;/div&gt;
  );
}</code></pre>
<p><code>condition &amp;&amp; element</code> renders the element only when
the condition is true, and renders nothing at all when it's false — a
clean way to express "show this, or don't," when there's no meaningful
alternative content for the false case (unlike the ternary example,
which had a real "else" branch).</p>

<h2>Example 3: an if statement above the return, for bigger decisions</h2>
<pre><code>function Page({ user }) {
  if (!user) {
    return &lt;p&gt;Loading...&lt;/p&gt;;
  }
  return &lt;h1&gt;Welcome, {user.name}!&lt;/h1&gt;;
}</code></pre>
<p>When the decision is more substantial than one small piece of markup —
here, an entirely different component output depending on whether data
has loaded yet — a plain <code>if</code> before the <code>return</code>
is clearer than trying to cram the whole decision into a ternary.</p>
""",
    },
    {
        "slug": "rendering-lists",
        "summary": "Turning an array of data into an array of elements with .map() — and why the key prop isn't optional.",
        "body": """
<p>To render a list, use JavaScript's <code>.map()</code> (from the
JavaScript Arrays lesson) to turn an array of data into an array of JSX
elements.</p>

<h2>Example: a list of students</h2>
<pre><code>function StudentList({ students }) {
  return (
    &lt;ul&gt;
      {students.map((s) => (
        &lt;li key={s.id}&gt;{s.name} — {s.track}&lt;/li&gt;
      ))}
    &lt;/ul&gt;
  );
}

// For students = [{id: 1, name: 'Ada', track: 'Frontend'},
//                  {id: 2, name: 'Chidi', track: 'Cybersecurity'}]
// renders a bulleted list with both students' names and tracks.</code></pre>

<h2>Why the key prop matters, not just React being picky</h2>
<p>Each item needs a unique <code>key</code> prop — here,
<code>s.id</code> — so React can track exactly which rendered item
corresponds to which piece of data across re-renders, especially when
items get added, removed, or reordered. Using the array's index as a key
(<code>key={i}</code>) instead of a real id looks fine at first, but
breaks in a specific way once the list order can change: React starts
matching the wrong data to the wrong rendered element, since the index
stayed the same even though what's actually at that position changed.
Prefer a real, stable id whenever one exists — the array index only as a
genuine last resort, when the list itself never reorders or changes.</p>
""",
    },
]


def deepen_react_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="react")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0030_deepen_js_content"),
    ]

    operations = [
        migrations.RunPython(deepen_react_content, noop),
    ]
