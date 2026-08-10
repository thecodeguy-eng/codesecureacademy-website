from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to React",
        "slug": "introduction",
        "order": 1,
        "summary": "A JavaScript library for building UIs out of reusable components.",
        "body": """
<p>React is a JavaScript library for building user interfaces out of small, reusable
<strong>components</strong> &mdash; each one a JavaScript function that returns what should
appear on screen. Instead of manually updating the page when data changes, you describe what
the UI should look like for the current data, and React figures out how to update the real
page to match.</p>
<p>React code is normally compiled by a build tool before it reaches the browser, so these
examples are shown read-only rather than live-editable.</p>
""",
        "example_code": """function App() {
  return <h1>Hello, world!</h1>;
}""",
        "expected_output": "Renders an <h1> reading \"Hello, world!\" wherever <App /> is mounted.",
    },
    {
        "title": "JSX",
        "slug": "jsx",
        "order": 2,
        "summary": "Writing HTML-like markup directly inside JavaScript.",
        "body": """
<p>JSX is the syntax that lets you write HTML-like markup inside a JavaScript function.
It isn't a string &mdash; it compiles down to regular JavaScript function calls that build
up the UI. Use curly braces <code>{ }</code> to drop a JavaScript expression (a variable, a
calculation, a function call) into the markup.</p>
""",
        "example_code": """function Greeting() {
  const name = "Ada";
  return <p>Hello, {name}! 2 + 2 is {2 + 2}.</p>;
}""",
        "expected_output": "Renders: Hello, Ada! 2 + 2 is 4.",
    },
    {
        "title": "Components & Props",
        "slug": "components-and-props",
        "order": 3,
        "summary": "Passing data into a component from its parent.",
        "body": """
<p>A component is just a function; <strong>props</strong> are the arguments you pass it,
written like HTML attributes: <code>&lt;Greeting name="Ada" /&gt;</code>. Inside the
component, they arrive as one object &mdash; <code>props.name</code>. This is how a single
component gets reused with different data each time.</p>
""",
        "example_code": """function Greeting(props) {
  return <p>Hello, {props.name}!</p>;
}

function App() {
  return (
    <div>
      <Greeting name="Ada" />
      <Greeting name="Chidi" />
    </div>
  );
}""",
        "expected_output": "Renders two paragraphs: \"Hello, Ada!\" and \"Hello, Chidi!\".",
    },
    {
        "title": "State with useState",
        "slug": "usestate",
        "order": 4,
        "summary": "Giving a component memory that persists between renders.",
        "body": """
<p><code>useState</code> gives a component a piece of data that persists across re-renders,
and a function to update it. Calling that update function tells React to re-run the
component and redraw it with the new value &mdash; this is the core mechanism behind any
interactive React UI.</p>
""",
        "example_code": """import { useState } from "react";

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Add</button>
    </div>
  );
}""",
        "expected_output": "Renders \"Count: 0\" with an Add button; each click increments the displayed count by 1.",
    },
    {
        "title": "Side Effects with useEffect",
        "slug": "useeffect",
        "order": 5,
        "summary": "Running code in response to a component rendering or its data changing.",
        "body": """
<p><code>useEffect</code> runs code after a component renders &mdash; fetching data,
subscribing to something, or manually touching the DOM. Its second argument, a
<strong>dependency array</strong>, controls when it re-runs: an empty array
<code>[]</code> means "only once, after the first render."</p>
""",
        "example_code": """import { useState, useEffect } from "react";

function Clock() {
  const [time, setTime] = useState(new Date().toLocaleTimeString());

  useEffect(() => {
    const id = setInterval(() => setTime(new Date().toLocaleTimeString()), 1000);
    return () => clearInterval(id);
  }, []);

  return <p>Current time: {time}</p>;
}""",
        "expected_output": "Renders the current time as text, updating once per second.",
    },
    {
        "title": "Handling Events",
        "slug": "handling-events",
        "order": 6,
        "summary": "Responding to clicks, typing, and other user interaction.",
        "body": """
<p>React event handlers are camelCase props &mdash; <code>onClick</code>,
<code>onChange</code>, <code>onSubmit</code> &mdash; set to a function. That function runs
whenever the event fires.</p>
""",
        "example_code": """function SearchBox() {
  function handleChange(e) {
    console.log("You typed:", e.target.value);
  }

  return <input type="text" onChange={handleChange} placeholder="Search..." />;
}""",
        "expected_output": "Logs \"You typed: <current value>\" to the console every time the input changes.",
    },
    {
        "title": "Conditional Rendering",
        "slug": "conditional-rendering",
        "order": 7,
        "summary": "Showing different markup depending on a condition.",
        "body": """
<p>Since JSX is just JavaScript, you can use normal JavaScript to decide what to render
&mdash; an <code>if</code> statement before the <code>return</code>, a ternary
(<code>condition ? a : b</code>) inline, or <code>&&</code> to render something only
when a condition is true.</p>
""",
        "example_code": """function Status({ loggedIn }) {
  return (
    <p>{loggedIn ? "Welcome back!" : "Please log in."}</p>
  );
}""",
        "expected_output": "<Status loggedIn={true} /> renders \"Welcome back!\"; <Status loggedIn={false} /> renders \"Please log in.\"",
    },
    {
        "title": "Rendering Lists",
        "slug": "rendering-lists",
        "order": 8,
        "summary": "Turning an array of data into an array of elements with .map().",
        "body": """
<p>To render a list, use JavaScript's <code>.map()</code> to turn an array of data into an
array of JSX elements. Each item needs a unique <code>key</code> prop, so React can track
which item is which across re-renders &mdash; usually an id, not the array index.</p>
""",
        "example_code": """function StudentList({ students }) {
  return (
    <ul>
      {students.map((s) => (
        <li key={s.id}>{s.name}</li>
      ))}
    </ul>
  );
}""",
        "expected_output": "For students = [{id: 1, name: 'Ada'}, {id: 2, name: 'Chidi'}], renders a bulleted list with items \"Ada\" and \"Chidi\".",
    },
]


def seed_react_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    frontend = Category.objects.get(slug="frontend")

    subject, _ = Subject.objects.update_or_create(
        slug="react",
        defaults={
            "category": frontend,
            "name": "React",
            "icon": "⚛️",
            "description": "A JavaScript library for building user interfaces out of reusable components.",
            "editor_language": "react",
            "order": 4,
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


def unseed_react_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="react").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0018_alter_subject_editor_language"),
    ]

    operations = [
        migrations.RunPython(seed_react_subject, unseed_react_subject),
    ]
