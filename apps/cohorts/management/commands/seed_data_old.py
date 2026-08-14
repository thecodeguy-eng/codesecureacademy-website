import datetime

from django.core.management.base import BaseCommand

from apps.cohorts.models import Cohort, Track
from apps.core.models import FAQ, SiteSettings


class Command(BaseCommand):
    help = (
        "Seeds placeholder tracks, cohorts, site stats, and FAQs so the site "
        "isn't empty locally. All prices/dates/seat counts are placeholders. "
        "Replace them with real numbers from Victory in the admin before launch."
    )

    def handle(self, *args, **options):
        today = datetime.date.today()

        tracks = [
            {
                "slug": "frontend",
                "name": "Frontend Development",
                "tagline": "Build fast, accessible interfaces with real projects, not just tutorials.",
                "description": (
                    "Every website and app you've ever used started as an idea someone turned into "
                    "pixels on a screen. In this track, you'll do the same, starting from a blank "
                    "file and ending with a real, working interface you built yourself. No "
                    "lorem-ipsum practice sites: you'll build the same kind of interface companies "
                    "actually ship, with the same tools frontend developers use every day."
                ),
                "highlights": "HTML, CSS & modern JavaScript\nA frontend framework (React)\nResponsive, accessible UI\nGit & deployment workflow\nA portfolio-ready capstone project",
                "why_join": (
                    "You'll ship a real, working project, not a tutorial you forget by next week\n"
                    "Learn the exact stack (HTML, CSS, JavaScript, React) that's actually hiring right now\n"
                    "A cohort and a WhatsApp community, not a lonely login screen\n"
                    "Walk away with something you can put in a portfolio and show off"
                ),
                "cover_image_url": "https://images.unsplash.com/photo-1542831371-29b0f74f9713?w=1200&q=80&fm=jpg&fit=crop",
            },
            {
                "slug": "backend",
                "name": "Backend Development",
                "tagline": "APIs, databases, and the systems that actually run in production.",
                "description": (
                    "Every app people love is powered by something they never see: the backend. "
                    "In this track, you'll build the APIs, databases, and systems that make frontend "
                    "interfaces actually work, and learn to think about what happens when real "
                    "traffic hits your server, not just when it's running on your laptop."
                ),
                "highlights": "Server-side fundamentals\nRelational databases & queries\nREST API design\nAuthentication & security basics\nDeploying a live API",
                "why_join": (
                    "Build APIs a real frontend app can actually talk to\n"
                    "Learn databases, authentication, and deployment: the parts most tutorials skip\n"
                    "Understand what's really happening behind every app you use\n"
                    "Finish with a live, deployed API you built from scratch"
                ),
                "cover_image_url": "https://miro.medium.com/v2/resize:fit:1400/1*-RScwHg4ilGiM7cpK4xVpg.png",
            },
            {
                "slug": "cybersecurity",
                "name": "Cybersecurity",
                "tagline": "Think like an attacker so you can defend like a professional.",
                "description": (
                    "Attackers don't wait for permission, and neither should your instincts. This "
                    "track teaches you to think like the people trying to break in, so you can build "
                    "and defend like someone who already knows their next move."
                ),
                "highlights": "Networking & security fundamentals\nCommon web vulnerabilities (OWASP)\nHands-on lab exercises\nSecurity tooling\nIncident response basics",
                "why_join": (
                    "Learn to spot the vulnerabilities most developers miss\n"
                    "Hands-on labs, not just slides about hackers\n"
                    "Understand the OWASP Top 10 well enough to explain it to anyone\n"
                    "Build the habit of asking 'what could go wrong here?' on every project after this"
                ),
                "cover_image_url": "https://images.unsplash.com/photo-1633265486064-086b219458ec?w=1200&q=80&fm=jpg&fit=crop",
            },
            {
                "slug": "graphic_design",
                "name": "Graphic Design",
                "tagline": "Design that communicates: brand, layout, and visual systems.",
                "description": (
                    "Good design isn't decoration, it's communication. In this track, you'll learn "
                    "to turn a blank canvas into something that actually says what it's supposed to "
                    "say, using the same tools and process working designers use on real client briefs."
                ),
                "highlights": "Design principles & typography\nIndustry-standard tools\nBrand identity systems\nLayout & visual hierarchy\nA client-brief portfolio piece",
                "why_join": (
                    "Work real, client-style briefs, not just 'design a poster' exercises\n"
                    "Learn the industry-standard tools employers actually expect\n"
                    "Build a portfolio piece you'd be proud to show a client\n"
                    "Understand brand and layout systems, not just how to make one thing look nice"
                ),
                "cover_image_url": "https://images.unsplash.com/photo-1716471330463-f475b00f0506?w=1200&q=80&fm=jpg&fit=crop",
            },
        ]

        for data in tracks:
            slug = data.pop("slug")
            track, created = Track.objects.update_or_create(slug=slug, defaults=data)
            status = "created" if created else "updated"
            self.stdout.write(f"Track '{track.name}' {status}")

            if not track.cohorts.exists():
                Cohort.objects.create(
                    track=track,
                    start_date=today + datetime.timedelta(days=21),
                    end_date=today + datetime.timedelta(days=21 + 56),
                    price_naira=150000,  # PLACEHOLDER — replace with the real per-track price
                    seat_count=25,  # PLACEHOLDER — replace with the real seat count
                )
                self.stdout.write(self.style.WARNING(f"  -> added a PLACEHOLDER cohort for {track.name} (fake price/dates/seats)"))

        # Left at 0 deliberately — these render as real trust stats on the
        # homepage, so they should never ship with made-up numbers. The
        # stats bar hides itself until an admin sets real values.
        SiteSettings.load()

        faqs = [
            ("How do I pay for a cohort?", "Pick a track, log in, and check out securely with Paystack. Card or bank transfer both work."),
            ("What happens if my cohort fills up?", "Join the waitlist and we'll email you the moment a seat opens for the next cohort."),
            ("How do I get into the WhatsApp group?", "The moment your payment is confirmed, you'll get the invite link by email and on-screen."),
            ("Do I need prior experience to join a track?", "No. Each track starts from the fundamentals and builds up from there. You just need to be ready to put in the work."),
            ("Do I need my own laptop?", "Yes, you'll need a laptop capable of running the tools for your track. We'll share the specific requirements once you're enrolled."),
            ("What's your refund policy?", "Check our Terms of Service page for the full refund policy."),
            ("Is the marketplace open to everyone?", "Yes, anyone can browse and buy. Selling requires an approved seller account, open to students and outside sellers alike."),
        ]
        for question, answer in faqs:
            FAQ.objects.get_or_create(question=question, defaults={"answer": answer})

        self.stdout.write(self.style.SUCCESS("Seed data ready. Replace placeholder prices/dates/seats in the admin before launch."))
