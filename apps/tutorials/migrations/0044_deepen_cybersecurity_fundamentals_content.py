from django.db import migrations

ARTICLES = [
    {
        "slug": "what-is-cybersecurity",
        "summary": "Protecting systems, networks, and data from unauthorized access or damage — the range of specialties inside the field.",
        "body": """
<p>Cybersecurity is the practice of protecting computers, networks, and
data from unauthorized access, damage, or theft. It spans a huge range of
work: securing a company's servers, writing code that resists attack,
teaching people to spot a phishing email, and responding when something
has already gone wrong.</p>

<h2>Example: three different security roles</h2>
<ul>
<li>A <strong>SOC analyst</strong> watches live traffic and alerts for
signs of an ongoing attack.</li>
<li>A <strong>penetration tester</strong> is paid, with explicit written
permission, to break into a system on purpose so its owner learns about
the hole before a real attacker does.</li>
<li>A <strong>security engineer</strong> builds the defenses the other
two roles rely on.</li>
</ul>
<p>This subject covers the foundational concepts every one of those roles
builds on, before any specific tool or technique.</p>
""",
    },
    {
        "slug": "cia-triad",
        "summary": "Confidentiality, Integrity, and Availability — the three goals nearly every security control exists to protect.",
        "body": """
<p>Almost every security control exists to protect one of three things,
together called the CIA triad.</p>

<h2>Example: the same system, three different failure modes</h2>
<ul>
<li><strong>Confidentiality</strong> — only authorized people can see the
data. Fails when: an attacker reads private messages they shouldn't be
able to.</li>
<li><strong>Integrity</strong> — the data hasn't been tampered with.
Fails when: someone silently edits a payment amount in transit.</li>
<li><strong>Availability</strong> — authorized people can actually access
the system when they need it. Fails when: a flood of fake traffic takes a
site offline for real users.</li>
</ul>
<p>A useful habit: when evaluating any security decision, ask which of
the three it's protecting — and whether it might be quietly trading off
one for another. Encrypting every field in a database, for instance,
strongly protects confidentiality but can hurt availability if it makes
the system too slow to use under real load.</p>
""",
    },
    {
        "slug": "common-threats",
        "summary": "Malware, phishing, and social engineering — the most common ways attackers actually get in, and why people, not just software, are the target.",
        "body": """
<p><strong>Malware</strong> is software designed to harm or exploit a
system — viruses, ransomware, spyware.</p>

<h2>Example: how a typical attack actually starts</h2>
<p>An employee receives an email that looks exactly like it's from IT,
asking them to "verify their password" through a link. The link leads to
a fake login page that looks identical to the real one. The employee
types their real password in — and now the attacker has it, with zero
malware, zero exploited software vulnerability, and zero technical
sophistication involved at all.</p>
<p>That's <strong>phishing</strong>: tricking someone into handing over
credentials or clicking a malicious link, disguised as something
legitimate. <strong>Social engineering</strong> is the broader category
both belong to — manipulating people, not just software, into doing
something insecure. Most real breaches start with a person, not a purely
technical flaw, which is exactly why security awareness training matters
as much as any firewall or antivirus tool.</p>
""",
    },
    {
        "slug": "passwords-and-authentication",
        "summary": "What makes a password strong, and why multi-factor authentication is the single highest-impact step most people can take.",
        "body": """
<p>A strong password is long and unpredictable — length matters more
than clever substitutions like "P@ssw0rd", which attackers' cracking
tools already expect and check for automatically.</p>

<h2>Example: two logins, one meaningfully safer</h2>
<pre><code>Login A: password only
  -> a leaked password (from any breach, anywhere) grants full access

Login B: password + MFA (a code from your phone)
  -> the same leaked password alone is no longer enough to get in</code></pre>
<p><strong>Multi-factor authentication (MFA)</strong> adds a second proof
of identity beyond a password — a code from your phone, a fingerprint —
so a leaked password alone isn't enough to break in. A password manager
lets you use a unique, random password per site without having to
memorize any of them, removing the temptation to reuse the same password
everywhere (which is exactly what makes one breach elsewhere dangerous to
you specifically). Enabling MFA is one of the single highest-impact
security steps an individual can take, for a small amount of daily
friction in return.</p>
""",
    },
    {
        "slug": "encryption-basics",
        "summary": "Scrambling data so only someone with the right key can read it — symmetric vs. asymmetric, and a toy example of the idea.",
        "body": """
<p>Encryption transforms readable data (plaintext) into scrambled data
(ciphertext) using a key — only someone with the matching key can reverse
it.</p>

<h2>Example: a very old, weak illustration of the idea</h2>
<pre><code>plaintext: HELLO
shift by 3
ciphertext: KHOOR</code></pre>
<p>Each letter shifted 3 places forward in the alphabet: H→K, E→H, L→O,
L→O, O→R. This is a Caesar cipher — genuinely ancient, and never used for
real security today (it's trivially crackable), but it illustrates the
core idea correctly at a tiny scale: apply a rule with a key, and reverse
it with the same key.</p>

<h2>Symmetric vs. asymmetric</h2>
<p><strong>Symmetric</strong> encryption uses the same key to lock and
unlock — fast, but both sides need to already share that secret key
somehow. <strong>Asymmetric</strong> encryption uses a public key to lock
and a separate private key to unlock, which is exactly how HTTPS
establishes a secure connection with a server you've never spoken to
before, without needing to have shared a secret in advance.</p>
""",
    },
    {
        "slug": "firewalls-and-network-security",
        "summary": "Controlling what traffic is allowed in and out of a network — and why a firewall alone isn't a complete defense.",
        "body": """
<p>A firewall inspects network traffic and blocks or allows it based on
rules — e.g. "allow web traffic on port 443, block everything else."</p>

<h2>Example: what a firewall stops, and what it doesn't</h2>
<p>A firewall correctly blocks an unsolicited connection attempt from a
random unknown IP address on an unused port — traffic that clearly
shouldn't be reaching this server at all. It does <em>not</em> stop an
attack that looks like legitimate traffic on an allowed port (a
compromised web application receiving a malicious but well-formed HTTP
request), and it does <em>not</em> stop an attacker who's already gotten
in through a phished employee's own valid credentials — that traffic
looks completely normal from the firewall's point of view.</p>
<p>This is why real network security layers several defenses rather than
relying on any single one — a firewall is a genuinely useful first line
of defense, not a complete one on its own.</p>
""",
    },
    {
        "slug": "owasp-top-10",
        "summary": "The most common categories of security flaws found in real web applications, with a concrete SQL injection example and its fix.",
        "body": """
<p>OWASP publishes a regularly-updated list of the most common web
application vulnerabilities. One you'll run into constantly as a
developer:</p>

<h2>Example: SQL injection, vulnerable vs. fixed</h2>
<pre><code># Vulnerable — user input is glued directly into the query string
query = f"SELECT * FROM users WHERE username = '{username}'"

# Safe — the database driver keeps the value separate from the query itself
cursor.execute("SELECT * FROM users WHERE username = %s", [username])</code></pre>
<p>The vulnerable version lets an attacker end the string early and
append their own SQL by typing something like <code>' OR '1'='1</code>
into the username field. The parameterized version treats the input
purely as data, no matter what it contains — the database driver never
lets it become part of the executable query structure at all. This is
exactly the same "never trust the browser or the input alone" principle
the Forms lessons across HTML, PHP, and Django all raise from a different
angle — here it's the specific, concrete consequence of skipping it.</p>
""",
    },
    {
        "slug": "staying-safe-online",
        "summary": "Practical habits that block most everyday attacks — a short, high-impact checklist worth actually following.",
        "body": """
<p>A short, high-impact checklist, in rough order of impact:</p>

<h2>Example: the habits that actually matter</h2>
<ul>
<li>Use a password manager and a unique, long password per site — not a
memorable one reused everywhere.</li>
<li>Turn on multi-factor authentication everywhere it's offered.</li>
<li>Keep software and your OS updated — patches often fix known,
publicly-documented security holes.</li>
<li>Be skeptical of unexpected links or attachments, even from people you
know — their account may be the one that's already compromised.</li>
<li>Back up important data somewhere an attacker who compromises your
main device can't also reach.</li>
</ul>
<p>None of this is exotic. Most real-world breaches succeed because a
basic habit like one of these was skipped, not because of some
exotic zero-day exploit nobody could have anticipated — which is
genuinely good news, since it means the highest-impact defenses are also
the most achievable ones.</p>
""",
    },
]


def deepen_cybersecurity_fundamentals_content(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    subject = Subject.objects.get(slug="cybersecurity-fundamentals")
    for data in ARTICLES:
        Article.objects.filter(subject=subject, slug=data["slug"]).update(
            summary=data["summary"], body=data["body"]
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0043_deepen_django_content"),
    ]

    operations = [
        migrations.RunPython(deepen_cybersecurity_fundamentals_content, noop),
    ]
