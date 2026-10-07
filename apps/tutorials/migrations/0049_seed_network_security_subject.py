from django.db import migrations

ARTICLES = [
    {
        "title": "What is a Network, Really?",
        "slug": "what-is-a-network",
        "order": 1,
        "summary": "IP addresses, packets, and routers, the basics everything else in this subject builds on.",
        "body": """
<p>A network is just a set of devices that can send each other data. Every device on a
network gets an <strong>IP address</strong>, a numeric label like <code>192.168.1.14</code>
that works like a postal address, so traffic knows where to go. Data doesn't travel as one
big chunk, it's broken into <strong>packets</strong>, small pieces that each carry a bit of
the data plus addressing information, sent separately and reassembled at the other end.</p>
<p>A <strong>router</strong> is the device that actually moves packets between networks,
deciding the next hop for each one based on its destination address. Your home router does
this between your devices and your internet provider; the internet itself is really just an
enormous chain of routers doing the same thing, hop by hop.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "The OSI Model, Just Enough to Be Useful",
        "slug": "osi-model",
        "order": 2,
        "summary": "A 7-layer way of thinking about networking that shows up constantly in security tooling and job interviews.",
        "body": """
<p>The OSI model splits networking into 7 layers, from the physical cable (layer 1) up to
the application a user actually sees (layer 7). You don't need to memorize all 7 to be
useful, but three come up constantly in security work:</p>
<ul>
<li><strong>Layer 3, Network</strong> &mdash; IP addresses and routing live here. This is
where firewalls make most of their allow/block decisions.</li>
<li><strong>Layer 4, Transport</strong> &mdash; TCP and UDP live here, deciding how
reliably data gets delivered (more on this in the next article).</li>
<li><strong>Layer 7, Application</strong> &mdash; HTTP, DNS, email, the actual protocols
apps use. Most of the vulnerabilities in the Web Application Security subject live here.</li>
</ul>
<p>When a tool or a job description says "layer 7 firewall" or "layer 3 switch," this is
the vocabulary it's drawing from.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "TCP vs UDP",
        "slug": "tcp-vs-udp",
        "order": 3,
        "summary": "The two ways data actually travels across a network, and why the choice matters.",
        "body": """
<p><strong>TCP</strong> is reliable: before sending data, it establishes a connection (the
well-known "three-way handshake"), confirms every piece arrived, and resends anything lost.
That reliability has a cost in speed and overhead, so TCP is used where correctness matters
more than speed, loading a web page, sending an email.</p>
<p><strong>UDP</strong> skips all of that. It just sends the packets and moves on, no
handshake, no guaranteed delivery, no resending lost data. That makes it faster and lighter,
which is why it's used where speed matters more than perfect delivery, video calls, online
games, DNS lookups, a dropped frame or two is barely noticeable, but a laggy call is
unusable.</p>
<p>This distinction matters for security too: a lot of scanning and denial-of-service
techniques specifically exploit the differences in how each protocol handles unexpected or
malformed traffic.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Firewalls, Deeper Than the Basics",
        "slug": "firewalls-deeper",
        "order": 4,
        "summary": "Stateless vs stateful filtering, and what a real firewall rule actually looks like.",
        "body": """
<p>Cybersecurity Fundamentals introduced firewalls as traffic rules. Here's what a rule
actually looks like, and the one distinction that matters most: <strong>stateless</strong>
vs <strong>stateful</strong> filtering.</p>
<p>A stateless firewall checks each packet in isolation against its rule list, every single
time, with no memory of what came before. A stateful firewall tracks active connections, so
once it's allowed the first packet of a legitimate connection, it automatically allows the
return traffic for that same connection without re-checking every rule. Almost every modern
firewall, including the one built into your OS, is stateful, it's both faster and more
secure, since it can spot traffic that doesn't belong to any connection it actually opened.</p>
""",
        "example_code": """# A typical stateful firewall rule, in a common plain-English style:
ALLOW   tcp   port 443   from any           # let HTTPS traffic in from anywhere
ALLOW   tcp   port 22    from 10.0.0.0/24   # SSH, but only from this internal network
DENY    all   all        from any           # block everything else by default""",
        "expected_output": "The order matters: rules are usually checked top to bottom, and the first match wins. That final DENY-all rule is called a default-deny policy, explicitly blocking anything not already allowed above it, rather than hoping nothing dangerous was missed.",
    },
    {
        "title": "VPNs and Why They Matter",
        "slug": "vpns",
        "order": 5,
        "summary": "Encrypting your traffic and hiding it inside a trusted tunnel.",
        "body": """
<p>A VPN (Virtual Private Network) creates an encrypted tunnel between your device and a
VPN server, routing your traffic through it. Two main reasons this matters:</p>
<ul>
<li><strong>Privacy on untrusted networks</strong> &mdash; on public WiFi, anyone else on
that network could potentially intercept unencrypted traffic. A VPN encrypts everything
leaving your device, so even on a hostile network, what's visible is scrambled.</li>
<li><strong>Secure access to private networks</strong> &mdash; companies use VPNs so
remote employees can reach internal systems (databases, internal tools) that are never
exposed to the public internet directly, as if they were plugged in at the office.</li>
</ul>
<p>A VPN doesn't make you anonymous, and it doesn't protect you from, say, a phishing link
you click, it specifically protects the traffic between your device and the VPN server.
Knowing exactly what a security tool does and doesn't cover is as important as knowing how
to use it.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Wireless Network Security",
        "slug": "wireless-network-security",
        "order": 6,
        "summary": "Why WPA3 matters, and the WiFi habits that actually protect you.",
        "body": """
<p>WiFi traffic travels through the air, so anyone nearby can technically receive it, the
only thing stopping them from reading it is encryption. <strong>WPA3</strong> is the current
WiFi security standard, replacing the older WPA2 (still common) and the now-broken WEP
(should never be used). If a router's admin panel offers WPA3, use it; WPA2 with a strong
password is still reasonable, WEP is not meaningfully secure at all.</p>
<p>Beyond the encryption standard, a few habits matter: change the router's default admin
password (default credentials for most router models are public knowledge), use a long WiFi
password rather than a short memorable one, and keep router firmware updated, router
vulnerabilities are a genuinely common way attackers get into home networks.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
    {
        "title": "Network Scanning & Reconnaissance",
        "slug": "network-scanning",
        "order": 7,
        "summary": "How security professionals map out a network, and why the same tools serve both attackers and defenders.",
        "body": """
<p>Before securing or attacking a network, you first need to know what's actually on it.
<strong>Network scanning</strong> tools send probe traffic to a range of addresses and
report what responds, live hosts, open ports, sometimes even the software version running
behind a port. <code>nmap</code> is the standard open-source tool for this.</p>
""",
        "example_code": "# Scan a network range for live hosts and open ports\nnmap -sV 192.168.1.0/24\n\n# Scan a single host more thoroughly\nnmap -A 192.168.1.14",
        "expected_output": "nmap reports which hosts on that range responded, which ports are open on each, and (with -sV) its best guess at what software/version is listening on each port. A penetration tester runs this to find what's reachable before testing it further. A defender runs the exact same command against their own network, to spot anything exposed that shouldn't be.",
    },
    {
        "title": "Securing a Home or Small Office Network",
        "slug": "securing-a-network",
        "order": 8,
        "summary": "A practical checklist that closes most of the common ways a small network gets compromised.",
        "body": """
<p>A short, practical checklist, the small-network equivalent of the "Staying Safe Online"
checklist in Cybersecurity Fundamentals:</p>
<ul>
<li>Change the router's default admin username and password.</li>
<li>Use WPA3 (or WPA2 at minimum) with a long WiFi password, never WEP.</li>
<li>Keep router firmware updated, check the admin panel periodically.</li>
<li>Turn off remote administration on the router unless you specifically need it.</li>
<li>Put IoT devices (smart plugs, cameras) on a separate guest network from your main
devices, so a compromised smart bulb can't reach your laptop.</li>
<li>Disable UPnP on the router unless something specifically requires it, it can
automatically open ports without asking.</li>
</ul>
<p>None of this requires specialized tools, just going through the router's own admin panel
once and changing what's still sitting on factory defaults.</p>
""",
        "example_code": "",
        "expected_output": "",
    },
]


def seed_network_security_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Category = apps.get_model("tutorials", "Category")
    Article = apps.get_model("tutorials", "Article")

    cybersecurity = Category.objects.get(slug="cybersecurity")

    subject, _ = Subject.objects.update_or_create(
        slug="network-security",
        defaults={
            "category": cybersecurity,
            "name": "Network Security",
            "icon": "\U0001F6F0️",
            "description": "How networks actually work, and how to secure them, from IP addresses to firewalls to VPNs.",
            "editor_language": "none",
            "order": 10,
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


def unseed_network_security_subject(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug="network-security").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0048_seed_web_security_subject"),
    ]

    operations = [
        migrations.RunPython(seed_network_security_subject, unseed_network_security_subject),
    ]
