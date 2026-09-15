from django.core.management.base import BaseCommand

from apps.cohorts.models import Track
from apps.lessons.models import Lesson

CYBERSECURITY_LESSONS = [
    {
        "slug": "welcome-to-the-track",
        "title": "Welcome to the Cybersecurity Track",
        "summary": "What this track covers and how to get the most out of it.",
        "body": """
<p>Welcome — you're enrolled, and this is where the actual work starts. This
track is built around one idea: security only makes sense once you understand
what you're defending and who you're defending it from. Everything else,
tools, commands, checklists, is downstream of that.</p>
<p>Over the coming weeks you'll move through the fundamentals in this order:
core security concepts, how to work comfortably on the command line, how to
set up a safe environment to practice in, and then into hands-on offensive
and defensive exercises with your cohort.</p>
<ul>
  <li>Work through lessons in order — later ones assume the earlier ones.</li>
  <li>Mark each lesson complete as you finish it, so you can see your progress here and pick up where you left off.</li>
  <li>Bring questions to your cohort's WhatsApp group. You're not doing this alone.</li>
</ul>
""",
    },
    {
        "slug": "cia-triad",
        "title": "The CIA Triad: Confidentiality, Integrity, Availability",
        "summary": "The three properties almost every security decision is trying to protect.",
        "body": """
<p>Before any tool or technique, security has a goal, and that goal is
usually described in terms of three properties, together called the
<strong>CIA triad</strong>:</p>
<ul>
  <li><strong>Confidentiality</strong> — only the people who should see data can see it. A password database leaking is a confidentiality failure.</li>
  <li><strong>Integrity</strong> — data hasn't been tampered with, whether by an attacker or by accident. A bank balance silently changing is an integrity failure.</li>
  <li><strong>Availability</strong> — the system works when it's supposed to. A server knocked offline by an attack is an availability failure.</li>
</ul>
<p>Almost every security control you'll learn about exists to protect one or
more of these. Encryption protects confidentiality. Checksums and digital
signatures protect integrity. Redundancy and rate-limiting protect
availability. When you're evaluating any new tool or practice later in this
track, it's worth asking: which of these three is it actually protecting,
and against what kind of failure?</p>
""",
    },
    {
        "slug": "threats-vulnerabilities-risk",
        "title": "Threats, Vulnerabilities, and Risk",
        "summary": "Three words that get used interchangeably but mean different things.",
        "body": """
<p>These three terms get mixed up constantly, but keeping them separate
makes it much easier to reason about security problems clearly:</p>
<ul>
  <li><strong>Vulnerability</strong> — a weakness. An out-of-date library, a
  misconfigured server, a password that's easy to guess. It exists whether
  or not anyone ever exploits it.</li>
  <li><strong>Threat</strong> — someone or something that could exploit a
  vulnerability. A threat isn't a flaw in your system; it's a source of
  potential harm, an attacker, a piece of malware, even an untrained
  employee who clicks the wrong link.</li>
  <li><strong>Risk</strong> — the actual likelihood and impact of a threat
  exploiting a vulnerability. A critical vulnerability that no realistic
  threat can reach is low risk. A minor vulnerability exposed directly to
  the internet, with attackers actively scanning for it, can be high risk.</li>
</ul>
<p>Security work is mostly risk management, not the pursuit of some
impossible "perfectly secure" state. You'll spend a lot of your time in this
track learning to spot vulnerabilities, but the professional skill is
prioritizing which ones actually matter given the real threats and the real
impact if they're exploited.</p>
""",
    },
    {
        "slug": "command-line-basics-for-security",
        "title": "Getting Comfortable on the Command Line",
        "summary": "The handful of commands you'll lean on constantly in security work.",
        "body": """
<p>Most security tooling assumes you're comfortable in a terminal, so this
lesson is a deliberately small, practical starting set rather than a full
Linux course. On a Linux or macOS terminal (or WSL on Windows), try these:</p>
<ul>
  <li><code>pwd</code> — print the directory you're currently in.</li>
  <li><code>ls -la</code> — list every file in the current directory, including hidden ones, with permissions.</li>
  <li><code>cd &lt;path&gt;</code> — move into a different directory.</li>
  <li><code>cat &lt;file&gt;</code> — print a file's contents to the screen.</li>
  <li><code>grep -r "text" .</code> — search recursively for a string in every file under the current directory.</li>
  <li><code>chmod</code> / <code>chown</code> — change a file's permissions or owner, both directly relevant to spotting misconfigurations later in this track.</li>
</ul>
<p>You don't need to memorize flags. What matters right now is losing the
hesitation to open a terminal at all, since nearly every exercise from here
on assumes you will.</p>
""",
    },
    {
        "slug": "safe-practice-lab",
        "title": "Setting Up a Safe Lab to Practice In",
        "summary": "Why you need an isolated environment before you run any security tool for real.",
        "body": """
<p>Before you run a scanner, an exploit, or anything else you'll learn later
in this track, you need somewhere safe to run it, never your main laptop,
and never a system you don't own or have explicit permission to test.</p>
<p>The standard approach is a <strong>virtual machine (VM)</strong>: a
simulated computer running inside your real one, isolated from your actual
files and network in a way you control. Two free options to get started
with:</p>
<ul>
  <li><strong>VirtualBox</strong> — free, cross-platform, the most common
  starting point for a first practice lab.</li>
  <li><strong>VMware Workstation Player</strong> — also free for personal
  use, a solid alternative.</li>
</ul>
<p>A common cohort setup is one VM running a security-focused Linux
distribution for practicing techniques, and a second, deliberately
vulnerable VM as a target, so you're always attacking a machine built for
exactly that purpose rather than anything real. Your cohort's WhatsApp group
is the right place to ask for the current recommended images once you're
ready to set this up.</p>
<p><strong>Rule that doesn't have exceptions:</strong> everything you try in
this track happens inside this isolated lab, or against a system you have
explicit written permission to test. Never against anything else.</p>
""",
    },
]


class Command(BaseCommand):
    help = "Seeds a small set of original Cybersecurity-track lessons as a working proof of concept."

    def handle(self, *args, **options):
        track = Track.objects.filter(slug="cybersecurity").first()
        if not track:
            self.stdout.write(self.style.ERROR("No Cybersecurity track found — run seed_data first."))
            return

        for order, data in enumerate(CYBERSECURITY_LESSONS):
            slug = data["slug"]
            lesson, created = Lesson.objects.update_or_create(
                track=track, slug=slug,
                defaults={
                    "title": data["title"], "summary": data["summary"],
                    "body": data["body"].strip(), "order": order,
                },
            )
            self.stdout.write(f"{'Created' if created else 'Updated'}: {lesson.title}")

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(CYBERSECURITY_LESSONS)} lessons for Cybersecurity."))
