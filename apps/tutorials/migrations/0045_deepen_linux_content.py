from django.db import migrations

ARTICLES = [
    {
        "slug": "introduction",
        "summary": "Why Linux matters for security work: it runs almost every server on the internet, and it's operated through the terminal.",
        "body": """
<p>Linux is a free, open-source operating system that runs the
overwhelming majority of servers, cloud infrastructure, and security
tooling — comfort with it is close to a requirement for cybersecurity
work, and genuinely useful for backend development too.</p>

<h2>Why the terminal, not a graphical interface</h2>
<p>Most servers run with no graphical desktop at all — connecting to one
remotely gives you a terminal and nothing else, so terminal fluency isn't
optional the way it can feel on a personal computer with a full desktop
environment. A <strong>terminal</strong> is a text interface where you
type commands instead of clicking icons; that's what this whole subject
covers, one command family at a time.</p>
""",
    },
    {
        "slug": "navigating-the-filesystem",
        "summary": "pwd, ls, and cd — finding out where you are, seeing what's around you, and moving between folders.",
        "body": """
<p><code>pwd</code> ("print working directory") shows where you
currently are. <code>ls</code> lists what's in the current folder.
<code>cd</code> changes directory.</p>

<h2>Example: a short session</h2>
<pre><code>$ pwd
$ ls -la
$ cd Documents
$ pwd</code></pre>
<p>The <code>-la</code> flags on <code>ls</code> are worth knowing
separately: <code>-l</code> switches to a detailed "long" listing (one
file per line, with permissions and size — you'll see this format again
in the Permissions lesson), and <code>-a</code> includes hidden files
(anything starting with a dot, like <code>.gitignore</code>, normally
hidden from a plain <code>ls</code>). <code>cd ..</code> goes up one
level from wherever you are; <code>cd ~</code> jumps straight to your
home folder no matter how deep you've navigated.</p>
""",
        "expected_output": """/home/ada
total 12
drwxr-xr-x  3 ada ada 4096 Aug 10 12:00 .
drwxr-xr-x 20 ada ada 4096 Aug 10 11:58 ..
drwxr-xr-x  2 ada ada 4096 Aug 10 12:00 Documents
/home/ada/Documents""",
    },
    {
        "slug": "working-with-files",
        "summary": "mkdir, touch, cp, mv, and rm — creating, copying, renaming, and removing, and why rm has no undo.",
        "body": """
<p><code>mkdir name</code> creates a folder; <code>touch name</code>
creates an empty file. <code>cp source dest</code> copies,
<code>mv source dest</code> moves (or renames — the same command does
both, since a rename is really just a move to a new name in the same
place).</p>

<h2>Example: building up a small project structure</h2>
<pre><code>$ mkdir project
$ touch project/notes.txt
$ cp project/notes.txt project/notes-backup.txt
$ mv project/notes.txt project/README.txt</code></pre>
<p>The result: a <code>project/</code> folder containing
<code>README.txt</code> and <code>notes-backup.txt</code> (the original
<code>notes.txt</code> was renamed, not duplicated, by that last
<code>mv</code>). <code>rm name</code> deletes a file — there's no
recycle bin at the command line, so it's genuinely permanent the moment
you press enter. Add <code>-r</code> to <code>rm</code>/<code>cp</code>
to work on an entire folder recursively — and be especially careful with
<code>rm -r</code>, since a mistyped path can delete far more than
intended with no confirmation prompt by default.</p>
""",
    },
    {
        "slug": "viewing-and-editing-files",
        "summary": "cat, less, and nano — reading and editing text without leaving the terminal.",
        "body": """
<p><code>cat file</code> dumps a whole file's contents to the screen —
fine for short files, unwieldy for long ones. <code>less file</code>
opens a scrollable, searchable viewer for longer files.</p>

<h2>Example: choosing the right tool for the file's size</h2>
<pre><code>$ cat README.txt
$ less deploy.log
$ nano README.txt</code></pre>
<p>Use <code>cat</code> for something short enough to fit on one screen;
switch to <code>less</code> the moment a file is longer than that — it
lets you scroll and search (press <code>/</code> then type to search,
<code>q</code> to quit) without flooding your terminal with hundreds of
lines at once. <code>nano</code> opens a simple in-terminal text editor
for quick edits, when a full IDE is overkill or simply unavailable, as is
often the case when connected to a remote server.</p>
""",
        "expected_output": "cat prints the file's full contents immediately; less opens it for scrollable, searchable reading; nano opens it for interactive editing directly in the terminal.",
    },
    {
        "slug": "permissions",
        "summary": "chmod and chown — controlling who can read, write, and execute a file, and why misconfigured permissions are a real security issue.",
        "body": """
<p>Every file has read/write/execute permissions for its owner, its
group, and everyone else. <code>ls -l</code> shows them as a string like
<code>-rwxr--r--</code>.</p>

<h2>Example: making a script executable</h2>
<pre><code>$ chmod 755 deploy.sh
$ chown ada:ada deploy.sh
$ ls -l deploy.sh</code></pre>
<p><code>chmod 755</code> sets permissions using three digits — owner
(7 = read+write+execute), group (5 = read+execute), everyone else
(5 = read+execute). <code>chown ada:ada</code> changes who owns the file.
Misconfigured permissions are a genuine, common source of real security
vulnerabilities — a config file containing secrets that's readable by
"everyone" when it should only be readable by its owner is a classic,
easily-overlooked mistake, and exactly the kind of thing a security
assessment specifically checks for.</p>
""",
        "expected_output": "-rwxr-xr-x 1 ada ada 128 Aug 10 12:00 deploy.sh",
    },
    {
        "slug": "processes",
        "summary": "ps, top, and kill — seeing what's running on a machine, and stopping something that's misbehaving.",
        "body": """
<p><code>ps aux</code> lists every running process. <code>top</code>
shows a live, auto-refreshing view of what's using CPU and memory right
now.</p>

<h2>Example: finding and stopping a specific process</h2>
<pre><code>$ ps aux | grep python
$ kill 4821</code></pre>
<p>The <code>grep</code> filters <code>ps</code>'s full output down to
just lines mentioning "python" — piping is covered properly in the next
lesson, but this is one of its most common real uses: a command produces
too much output, and a second command narrows it down to what you
actually care about. Once you've found the right process id (PID) —
<code>4821</code> here — <code>kill</code> stops it. Add <code>-9</code>
(<code>kill -9 4821</code>) to force-kill a process that isn't responding
to the normal, more polite request to stop.</p>
""",
        "expected_output": "The grep filters ps's output down to lines mentioning \"python\", e.g. showing PID 4821 — which the kill command then stops.",
    },
    {
        "slug": "piping-and-redirection",
        "summary": "Chaining commands together with | and sending output to a file with > — the idea that makes the command line genuinely powerful.",
        "body": """
<p>The pipe <code>|</code> feeds one command's output straight into
another's input — this is what makes the command line so powerful,
chaining small, focused tools into a bigger one.</p>

<h2>Example: filtering and logging</h2>
<pre><code>$ ls -la | grep ".txt"
$ echo "Deploy finished" >> deploy.log</code></pre>
<p>The first command lists only files whose names contain ".txt" — the
same <code>grep</code> filtering idea from the previous lesson, applied
to a directory listing instead of a process list. <code>&gt;</code>
redirects output into a file, overwriting whatever was there before;
<code>&gt;&gt;</code> (used above) appends instead, adding a new line to
<code>deploy.log</code> without erasing anything already logged — exactly
the distinction you want when writing to a log file that's supposed to
accumulate history rather than get wiped on every write.</p>
""",
        "expected_output": "The first command lists only files whose names contain \".txt\". The second appends a line to deploy.log without erasing what was already there.",
    },
    {
        "slug": "package-management",
        "summary": "Installing and updating software from the command line — apt on Debian/Ubuntu, and why updating first matters.",
        "body": """
<p>Most Linux distributions install and update software through a
package manager rather than downloading installers manually.
Debian/Ubuntu-based systems use <code>apt</code>.</p>

<h2>Example: installing a web server</h2>
<pre><code>$ sudo apt update
$ sudo apt install nginx</code></pre>
<p><code>sudo</code> runs the command with elevated (administrator)
privileges — required for actions like installing software that affect
the whole system, not just your own user account. <code>apt update</code>
refreshes the list of available package versions <em>before</em>
installing anything new — skipping this step is a common habit that
leads to installing an outdated version, since your local package list
can otherwise be stale. Only after that does <code>apt install nginx</code>
actually download and install the web server.</p>
""",
        "expected_output": "Refreshes the list of available packages, then downloads and installs the nginx web server.",
    },
]


def deepen_linux_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="linux")
    for data in ARTICLES:
        defaults = {"summary": data["summary"], "body": data["body"]}
        if "expected_output" in data:
            defaults["expected_output"] = data["expected_output"]
        Article.objects.filter(subject=subject, slug=data["slug"]).update(**defaults)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0044_deepen_cybersecurity_fundamentals_content"),
    ]

    operations = [
        migrations.RunPython(deepen_linux_content, noop),
    ]
