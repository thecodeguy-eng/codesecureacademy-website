from django.db import migrations

ARTICLES = [
    {
        "title": "What is Cybersecurity?",
        "slug": "what-is-cybersecurity",
        "order": 1,
        "summary": "Protecting systems, networks, and data from unauthorized access or damage.",
        "body": """
<p>Cybersecurity is the practice of protecting computers, networks, and data from
unauthorized access, damage, or theft. It spans a huge range of work: securing a company's
servers, writing code that resists attack, teaching people to spot a phishing email, and
responding when something has already gone wrong. This subject covers the foundational
concepts every other security topic builds on.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "The CIA Triad",
        "slug": "cia-triad",
        "order": 2,
        "summary": "Confidentiality, Integrity, and Availability — the three goals security defends.",
        "body": """
<p>Almost every security control exists to protect one of three things, together called the
CIA triad:</p>
<ul>
<li><strong>Confidentiality</strong> &mdash; only authorized people can see the data (e.g.
encryption, access controls).</li>
<li><strong>Integrity</strong> &mdash; the data hasn't been tampered with (e.g. checksums,
digital signatures).</li>
<li><strong>Availability</strong> &mdash; authorized people can actually access the system
when they need it (e.g. backups, protection against denial-of-service).</li>
</ul>
<p>A useful habit: when evaluating any security decision, ask which of the three it's
protecting &mdash; and whether it might be trading off one for another.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Common Threats: Malware, Phishing & Social Engineering",
        "slug": "common-threats",
        "order": 3,
        "summary": "The most common ways attackers actually get in.",
        "body": """
<p><strong>Malware</strong> is software designed to harm or exploit a system &mdash;
viruses, ransomware, spyware. <strong>Phishing</strong> tricks someone into handing over
credentials or clicking a malicious link, usually via a fake but convincing email or
message. <strong>Social engineering</strong> is the broader category both belong to:
manipulating people, not just software, into doing something insecure. Most breaches start
with a person, not a technical flaw &mdash; which is why security awareness matters as much
as any firewall.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Passwords & Authentication",
        "slug": "passwords-and-authentication",
        "order": 4,
        "summary": "What makes a password strong, and why multi-factor authentication matters.",
        "body": """
<p>A strong password is long and unpredictable &mdash; length matters more than clever
substitutions like "P@ssw0rd", which attackers' tools already expect. A password manager
lets you use a unique, random password per site without memorizing them.</p>
<p><strong>Multi-factor authentication (MFA)</strong> adds a second proof of identity beyond
a password &mdash; a code from your phone, a fingerprint &mdash; so a leaked password alone
isn't enough to break in. Enabling MFA is one of the single highest-impact security steps
an individual can take.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Encryption Basics",
        "slug": "encryption-basics",
        "order": 5,
        "summary": "Scrambling data so only someone with the right key can read it.",
        "body": """
<p>Encryption transforms readable data (plaintext) into scrambled data (ciphertext) using a
key &mdash; only someone with the matching key can reverse it. <strong>Symmetric</strong>
encryption uses the same key to lock and unlock; <strong>asymmetric</strong> encryption uses
a public key to lock and a separate private key to unlock, which is how HTTPS establishes a
secure connection without both sides needing to share a secret in advance.</p>
<p>A very old, weak example (never used for real security today) is a Caesar cipher, which
just shifts each letter by a fixed amount:</p>
""",
        "example_code": "plaintext: HELLO\nshift by 3\nciphertext: KHOOR",
        "expected_output": "Each letter shifted 3 places forward in the alphabet: H→K, E→H, L→O, L→O, O→R.",
    },
    {
        "title": "Firewalls & Network Security",
        "slug": "firewalls-and-network-security",
        "order": 6,
        "summary": "Controlling what traffic is allowed in and out of a network.",
        "body": """
<p>A firewall inspects network traffic and blocks or allows it based on rules &mdash; e.g.
"allow web traffic on port 443, block everything else." It's a first line of defense, not a
complete one: it can't stop an attack that looks like legitimate traffic, or one that comes
from a trusted user who's already been compromised (through phishing, for instance).
Network security layers several such defenses rather than relying on any single one.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "The OWASP Top 10 (Intro to Common Vulnerabilities)",
        "slug": "owasp-top-10",
        "order": 7,
        "summary": "The most common categories of security flaws found in real web applications.",
        "body": """
<p>OWASP publishes a regularly-updated list of the most common web application
vulnerabilities. Two you'll run into constantly as a developer:</p>
<p><strong>SQL Injection</strong> &mdash; building a database query by directly pasting
user input into it lets an attacker inject their own SQL. The fix is <strong>parameterized
queries</strong>, which keep user input separate from the query structure:</p>
""",
        "example_code": """# Vulnerable — user input is glued directly into the query string
query = f"SELECT * FROM users WHERE username = '{username}'"

# Safe — the database driver keeps the value separate from the query itself
cursor.execute("SELECT * FROM users WHERE username = %s", [username])""",
        "expected_output": "The vulnerable version lets an attacker end the string early and append their own SQL. The parameterized version treats the input purely as data, no matter what it contains.",
    },
    {
        "title": "Staying Safe Online",
        "slug": "staying-safe-online",
        "order": 8,
        "summary": "Practical habits that block most everyday attacks.",
        "body": """
<p>A short, high-impact checklist: use a password manager and unique passwords per site,
turn on multi-factor authentication everywhere it's offered, keep software and your OS
updated (patches often fix known security holes), be skeptical of unexpected links or
attachments even from people you know, and back up important data somewhere an attacker
who compromises your main device can't also reach. None of this is exotic &mdash; most
real-world breaches succeed because a basic habit like this was skipped, not because of an
exotic zero-day exploit.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
]


def seed_cybersecurity_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    cybersecurity = Category.objects.get(slug="cybersecurity")

    subject, _ = Subject.objects.update_or_create(
        slug="cybersecurity-fundamentals",
        defaults={
            "category": cybersecurity,
            "name": "Cybersecurity Fundamentals",
            "icon": "\U0001F6E1️",
            "description": "The core concepts behind defending systems, networks, and data from attackers.",
            "editor_language": "none",
            "order": 8,
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


def unseed_cybersecurity_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="cybersecurity-fundamentals").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0022_seed_flask_subject"),
    ]

    operations = [
        migrations.RunPython(seed_cybersecurity_subject, unseed_cybersecurity_subject),
    ]
