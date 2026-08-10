from django.db import migrations

ARTICLES = [
    {
        "title": "Introduction to Linux",
        "slug": "introduction",
        "order": 1,
        "summary": "Why Linux matters for security work: it runs almost every server on the internet.",
        "body": """
<p>Linux is a free, open-source operating system that runs the overwhelming majority of
servers, cloud infrastructure, and security tooling &mdash; comfort with it is close to a
requirement for cybersecurity work. Most of it is operated through a
<strong>terminal</strong>: a text interface where you type commands instead of clicking
icons. That's what this whole subject covers.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Navigating the Filesystem",
        "slug": "navigating-the-filesystem",
        "order": 2,
        "summary": "pwd, ls, and cd — finding out where you are and moving around.",
        "body": """
<p><code>pwd</code> ("print working directory") shows where you currently are.
<code>ls</code> lists what's in the current folder (add <code>-la</code> to include hidden
files and details). <code>cd</code> changes directory &mdash; <code>cd ..</code> goes up one
level, <code>cd ~</code> jumps to your home folder.</p>
""",
        "example_code": "$ pwd\n$ ls -la\n$ cd Documents",
        "expected_output": "/home/ada\ntotal 12\ndrwxr-xr-x  3 ada ada 4096 Aug 10 12:00 .\ndrwxr-xr-x 20 ada ada 4096 Aug 10 11:58 ..\ndrwxr-xr-x  2 ada ada 4096 Aug 10 12:00 Documents\n(then moves into Documents/)",
    },
    {
        "title": "Working with Files",
        "slug": "working-with-files",
        "order": 3,
        "summary": "mkdir, touch, cp, mv, and rm — creating, copying, and removing.",
        "body": """
<p><code>mkdir name</code> creates a folder; <code>touch name</code> creates an empty file.
<code>cp source dest</code> copies, <code>mv source dest</code> moves (or renames), and
<code>rm name</code> deletes &mdash; there's no recycle bin, so <code>rm</code> is
permanent. Add <code>-r</code> to <code>rm</code>/<code>cp</code> to work on an entire
folder recursively.</p>
""",
        "example_code": "$ mkdir project\n$ touch project/notes.txt\n$ cp project/notes.txt project/notes-backup.txt\n$ mv project/notes.txt project/README.txt",
        "expected_output": "Creates a project/ folder containing README.txt and notes-backup.txt (the original notes.txt was renamed).",
    },
    {
        "title": "Viewing & Editing Files",
        "slug": "viewing-and-editing-files",
        "order": 4,
        "summary": "cat, less, and nano — reading and editing text without leaving the terminal.",
        "body": """
<p><code>cat file</code> dumps a whole file's contents to the screen &mdash; fine for short
files. <code>less file</code> opens a scrollable, searchable viewer for longer ones (press
<code>q</code> to quit). <code>nano file</code> opens a simple in-terminal text editor for
quick edits, when a full IDE is overkill or unavailable.</p>
""",
        "example_code": "$ cat README.txt\n$ nano README.txt",
        "expected_output": "cat prints the file's full contents immediately; nano opens it for interactive editing in the terminal.",
    },
    {
        "title": "Permissions",
        "slug": "permissions",
        "order": 5,
        "summary": "chmod and chown — controlling who can read, write, and execute a file.",
        "body": """
<p>Every file has read/write/execute permissions for its owner, its group, and everyone
else. <code>ls -l</code> shows them as a string like <code>-rwxr--r--</code>.
<code>chmod</code> changes them (e.g. <code>chmod 755 script.sh</code> makes it
executable by the owner and readable by everyone), and <code>chown</code> changes who owns
the file. Misconfigured permissions are a real, common source of security vulnerabilities
&mdash; a file that's writable by "everyone" when it shouldn't be is a classic mistake.</p>
""",
        "example_code": "$ chmod 755 deploy.sh\n$ chown ada:ada deploy.sh\n$ ls -l deploy.sh",
        "expected_output": "-rwxr-xr-x 1 ada ada 128 Aug 10 12:00 deploy.sh",
    },
    {
        "title": "Processes",
        "slug": "processes",
        "order": 6,
        "summary": "ps, top, and kill — seeing what's running, and stopping it.",
        "body": """
<p><code>ps aux</code> lists every running process. <code>top</code> shows a live,
auto-refreshing view of what's using CPU and memory. <code>kill &lt;pid&gt;</code> stops a
process by its process ID (found via <code>ps</code> or <code>top</code>); add
<code>-9</code> to force-kill one that won't respond to a normal request to stop.</p>
""",
        "example_code": "$ ps aux | grep python\n$ kill 4821",
        "expected_output": "The grep filters ps's output down to lines mentioning \"python\", e.g. showing PID 4821 — which the kill command then stops.",
    },
    {
        "title": "Piping & Redirection",
        "slug": "piping-and-redirection",
        "order": 7,
        "summary": "Chaining commands together with | and sending output to a file with >.",
        "body": """
<p>The pipe <code>|</code> feeds one command's output straight into another's input &mdash;
this is what makes the command line so powerful, chaining small tools into a bigger one.
<code>&gt;</code> redirects output into a file (overwriting it); <code>&gt;&gt;</code>
appends instead of overwriting.</p>
""",
        "example_code": "$ ls -la | grep \".txt\"\n$ echo \"Deploy finished\" >> deploy.log",
        "expected_output": "The first command lists only files whose names contain \".txt\". The second appends a line to deploy.log without erasing what was already there.",
    },
    {
        "title": "Package Management",
        "slug": "package-management",
        "order": 8,
        "summary": "Installing and updating software from the command line.",
        "body": """
<p>Most Linux distributions install and update software through a package manager rather
than downloading installers manually. Debian/Ubuntu-based systems use
<code>apt</code>; Red Hat/Fedora-based systems use <code>dnf</code> (or the older
<code>yum</code>). Always update your package list before installing something new, so
you're pulling the latest available version.</p>
""",
        "example_code": "$ sudo apt update\n$ sudo apt install nginx",
        "expected_output": "Refreshes the list of available packages, then downloads and installs the nginx web server.",
    },
]


def seed_linux_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    cybersecurity = Category.objects.get(slug="cybersecurity")

    subject, _ = Subject.objects.update_or_create(
        slug="linux",
        defaults={
            "category": cybersecurity,
            "name": "Linux & the Command Line",
            "icon": "\U0001F427",
            "description": "The operating system behind most servers and security tooling, and how to drive it from the terminal.",
            "editor_language": "linux",
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


def unseed_linux_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="linux").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0023_seed_cybersecurity_fundamentals_subject"),
    ]

    operations = [
        migrations.RunPython(seed_linux_subject, unseed_linux_subject),
    ]
