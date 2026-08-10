from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "Google's toolkit for building one app that runs on mobile, web, and desktop — and why UI is described in code instead of dragged in a visual designer.",
        "body": """
<p>Flutter is a UI toolkit, written in Dart, for building
natively-compiled apps from a single codebase — the same code can ship to
iOS, Android, web, and desktop.</p>

<h2>Example: the entry point of a Flutter app</h2>
<pre><code>import 'package:flutter/material.dart';

void main() {
  runApp(
    const Center(
      child: Text('Hello, Flutter!', textDirection: TextDirection.ltr),
    ),
  );
}</code></pre>
<p>Renders a single line of centered text reading "Hello, Flutter!".</p>
<p>Instead of dragging elements in a visual designer, you describe your
UI in code as a tree of <strong>widgets</strong>, and Flutter draws it.
<code>runApp()</code> is the entry point that starts a Flutter app —
notice it's ultimately just calling Dart's own <code>main()</code>
function from the Dart tutorial, since Flutter apps are, underneath
everything, ordinary Dart programs.</p>
""",
    },
    {
        "slug": "widgets",
        "summary": "Everything in a Flutter UI is a widget, nested inside other widgets — and why that uniformity is actually the whole design.",
        "body": """
<p>In Flutter, <em>everything</em> is a widget — text, buttons, padding,
even layout itself.</p>

<h2>Example: widgets nested inside widgets</h2>
<pre><code>Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: const Text('My App')),
    body: const Padding(
      padding: EdgeInsets.all(16.0),
      child: Text('Welcome to my first screen!'),
    ),
  );
}</code></pre>
<p>Renders a screen with a top app bar titled "My App", and padded body
text below it.</p>
<p>You build a screen by nesting widgets inside each other's
<code>child</code> (or <code>children</code>) property, forming a tree —
here, <code>Scaffold</code> contains an <code>AppBar</code> and a
<code>Padding</code>, which itself contains a <code>Text</code>. Flutter
re-draws only the parts of that tree that actually changed when
something updates, which is part of why apps built this way stay fast
even as the UI grows more complex.</p>
""",
    },
    {
        "slug": "statelesswidget",
        "summary": "A widget that never changes once built — the simpler of Flutter's two core widget types.",
        "body": """
<p>A <code>StatelessWidget</code> describes UI that doesn't change over
time — given the same inputs, it always looks the same.</p>

<h2>Example: a reusable stateless widget</h2>
<pre><code>class GreetingCard extends StatelessWidget {
  final String name;
  const GreetingCard({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}</code></pre>
<p>Defines a reusable widget that displays "Hello, {name}!" — e.g.
<code>GreetingCard(name: 'Ada')</code> renders "Hello, Ada!".</p>
<p>You define it as a class extending <code>StatelessWidget</code>, and
override its <code>build()</code> method to return the widget tree.
Notice <code>name</code> is declared <code>final</code> — from the Dart
tutorial's Variables lesson — since a stateless widget's data, by
definition, never changes after it's built.</p>
""",
    },
    {
        "slug": "statefulwidget",
        "summary": "A widget that can change itself in response to interaction — split into two classes, and why setState is what actually triggers a redraw.",
        "body": """
<p>A <code>StatefulWidget</code> can redraw itself when its data changes —
a counter that goes up on tap, for example.</p>

<h2>Example: a tappable counter</h2>
<pre><code>class Counter extends StatefulWidget {
  const Counter({super.key});
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => setState(() => count++),
          child: const Text('Add'),
        ),
      ],
    );
  }
}</code></pre>
<p>Renders "Count: 0" with an "Add" button beneath it; each tap
increments the displayed count by 1.</p>
<p>It's split into two classes: the widget itself (<code>Counter</code>),
and a matching <code>State</code> class (<code>_CounterState</code>)
holding the mutable data. Calling <code>setState()</code> is the crucial
step — it tells Flutter "something changed, please rebuild this widget."
Changing <code>count</code> directly without wrapping it in
<code>setState()</code> would update the variable but never actually
redraw the screen, the exact same trap React's <code>useState</code>
lesson warns about with a plain variable instead of the state setter.</p>
""",
    },
    {
        "slug": "layout",
        "summary": "Arranging widgets horizontally, vertically, and with spacing using Row, Column, and Container.",
        "body": """
<p><code>Row</code> arranges its children left-to-right;
<code>Column</code> arranges them top-to-bottom.</p>

<h2>Example: three colored squares in a row</h2>
<pre><code>Widget build(BuildContext context) {
  return Row(
    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
    children: [
      Container(color: Colors.blue, width: 50, height: 50),
      Container(color: Colors.orange, width: 50, height: 50),
      Container(color: Colors.green, width: 50, height: 50),
    ],
  );
}</code></pre>
<p>Renders three evenly-spaced colored squares (blue, orange, green) in a
horizontal row.</p>
<p><code>Container</code> wraps a single child to add padding, margin,
size, or a background color — it's the Flutter equivalent of a styled
<code>&lt;div&gt;</code> from CSS. <code>mainAxisAlignment: MainAxisAlignment.spaceEvenly</code>
plays a nearly identical role to CSS flexbox's
<code>justify-content: space-evenly</code> — if you've read the CSS
tutorial's Flexbox lesson, this should feel like a direct parallel, not a
new concept.</p>
""",
    },
    {
        "slug": "user-input",
        "summary": "Buttons and text fields, and reacting to what the user does.",
        "body": """
<p><code>ElevatedButton</code>'s <code>onPressed</code> runs a function
when tapped. <code>TextField</code> collects typed text, usually paired
with a <code>TextEditingController</code>.</p>

<h2>Example: reading a text field's value on submit</h2>
<pre><code>final controller = TextEditingController();

Widget build(BuildContext context) {
  return Column(
    children: [
      TextField(controller: controller),
      ElevatedButton(
        onPressed: () => print('You typed: ${controller.text}'),
        child: const Text('Submit'),
      ),
    ],
  );
}</code></pre>
<p>Renders a text input above a "Submit" button; tapping Submit prints
whatever was typed into the field.</p>
<p>The <code>TextEditingController</code> is what lets your code read
back what the user typed — <code>controller.text</code> holds the
field's current value at any moment, similar in spirit to reading
<code>e.target.value</code> in the JavaScript/React event-handling
lessons, just structured as a persistent object here rather than a value
passed to an event handler each time.</p>
""",
    },
    {
        "slug": "styling",
        "summary": "TextStyle, colors, and rounded corners — Flutter's version of CSS.",
        "body": """
<p>Most widgets accept a <code>style</code> parameter.
<code>Text</code> takes a <code>TextStyle</code>; <code>Container</code>
takes a <code>BoxDecoration</code>.</p>

<h2>Example: a styled box with styled text inside</h2>
<pre><code>Widget build(BuildContext context) {
  return Container(
    padding: const EdgeInsets.all(12),
    decoration: BoxDecoration(
      color: Colors.blue,
      borderRadius: BorderRadius.circular(12),
    ),
    child: const Text(
      'Styled box',
      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
    ),
  );
}</code></pre>
<p>Renders a blue box with rounded corners containing bold, white, 18px
text reading "Styled box".</p>
<p>Compare this directly to the equivalent CSS from the CSS tutorial's
Box Model and Colors lessons — <code>borderRadius</code>,
<code>color</code>, <code>fontWeight</code> are all doing exactly the
same job CSS properties with nearly identical names would do on the web.
Flutter reinvents styling as Dart objects instead of a separate
stylesheet language, but the underlying visual concepts transfer directly
either way.</p>
""",
    },
    {
        "slug": "navigation",
        "summary": "Pushing a new screen onto the stack with Navigator — Flutter's model for moving between screens.",
        "body": """
<p>Flutter treats screens as a stack. <code>Navigator.push()</code> adds
a new screen on top, and <code>Navigator.pop()</code> removes the current
screen to go back.</p>

<h2>Example: navigating to a second screen</h2>
<pre><code>ElevatedButton(
  onPressed: () {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => const SecondScreen()),
    );
  },
  child: const Text('Go to Second Screen'),
)</code></pre>
<p>Tapping the button pushes a new screen (SecondScreen) on top of the
current one; a system back gesture or <code>Navigator.pop()</code>
returns to this screen.</p>
<p>The "stack" mental model is worth holding onto: think of screens like
a physical stack of cards — <code>push</code> adds a new card on top,
<code>pop</code> removes the top card to reveal what was underneath. This
is conceptually close to how Next.js's client-side <code>&lt;Link&gt;</code>
navigation works too, just with Flutter making the stack explicit as part
of its own API rather than mapping to browser history entries.</p>
""",
    },
]


def deepen_flutter_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="flutter")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0041_deepen_dart_content"),
    ]

    operations = [
        migrations.RunPython(deepen_flutter_content, noop),
    ]
