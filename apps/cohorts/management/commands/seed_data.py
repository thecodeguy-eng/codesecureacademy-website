import datetime

from django.core.management.base import BaseCommand

from apps.cohorts.models import Cohort, Track
from apps.core.models import FAQ, SiteSettings


class Command(BaseCommand):
    help = (
        "Seeds placeholder tracks, site stats, and FAQs so the site isn't "
        "empty locally, and a placeholder cohort for any track that has none "
        "yet. Safe to rerun any time — tracks and FAQs are updated in place, "
        "but an existing cohort is never touched (only created when a track "
        "has none), so real dates/price/seats set via the admin are never "
        "reset back to placeholders on a rerun."
    )

    def handle(self, *args, **options):
        today = datetime.date.today()

        tracks = [
            {
                "slug": "frontend",
                "name": "Frontend Development",
                "tagline": "Build fast, accessible interfaces, and ship a real project while you're at it.",
                "description": (
                    "Every website and app you've ever used started as an idea someone turned into "
                    "pixels on a screen. In this track, you'll do the same, starting from a blank "
                    "file and ending with a real, working interface you built yourself. No "
                    "lorem-ipsum practice sites: you'll build the same kind of interface companies "
                    "actually ship, with the same tools frontend developers use every day."
                ),
                "highlights": "HTML, CSS & modern JavaScript\nA frontend framework (React)\nResponsive, accessible UI\nGit & deployment workflow\nCapstone: a responsive, deployed multi-page web app",
                "why_join": (
                    "You'll ship a real, working project instead of just watching someone else build one\n"
                    "Learn the exact stack most frontend job listings ask for: HTML, CSS, JavaScript, and React\n"
                    "Walk away with something you can put in a portfolio and show off"
                ),
                "cover_image_url": "/static/img/photos/track-frontend.jpg",
            },
            {
                "slug": "backend",
                "name": "Backend Development",
                "tagline": "APIs, databases, and the systems that actually run in production.",
                "description": (
                    "Every app people love is powered by something they never see: the backend. "
                    "In this track, you'll build the APIs, databases, and systems that make frontend "
                    "interfaces actually work, and learn to think about what happens once real "
                    "traffic hits your server, past the point where it only has to work on your laptop."
                ),
                "highlights": "Server-side fundamentals\nRelational databases & queries\nREST API design\nAuthentication & security basics\nCapstone: a deployed REST API with authentication",
                "why_join": (
                    "Build APIs a real frontend app can actually talk to\n"
                    "Learn databases, authentication, and deployment: the parts most tutorials skip\n"
                    "Understand what's really happening behind every app you use\n"
                    "Finish with a live, deployed API you built from scratch"
                ),
                "cover_image_url": "/static/img/photos/track-backend.jpg",
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
                "highlights": "Networking & security fundamentals\nCommon web vulnerabilities (OWASP)\nHands-on lab exercises\nSecurity tooling\nCapstone: a documented vulnerability assessment report",
                "why_join": (
                    "Learn to spot the vulnerabilities most developers miss\n"
                    "Hands-on labs where you try the attack yourself, not slideshows about hackers\n"
                    "Understand the OWASP Top 10 well enough to explain it to anyone\n"
                    "Build the habit of asking 'what could go wrong here?' on every project after this"
                ),
                "cover_image_url": "/static/img/photos/track-cybersecurity.jpg",
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
                "highlights": "Design principles & typography\nFigma, Canva, and Adobe Photoshop\nBrand identity systems\nLayout & visual hierarchy\nCapstone: a full brand identity package for a mock client",
                "why_join": (
                    "Work real, client-style briefs instead of generic 'design a poster' exercises\n"
                    "Learn Figma, Canva, and Adobe Photoshop, the tools employers actually expect\n"
                    "Build a portfolio piece you'd be proud to show a client\n"
                    "Understand the brand and layout systems that hold a design together, not just one graphic"
                ),
                "cover_image_url": "/static/img/photos/track-graphic-design.jpg",
            },
        ]

        for data in tracks:
            slug = data.pop("slug")
            track, created = Track.objects.update_or_create(slug=slug, defaults=data)
            status = "created" if created else "updated"
            self.stdout.write(f"Track '{track.name}' {status}")

            # Only ever CREATES a cohort, and only when the track has none at
            # all — never touches an existing one. Real cohort dates/price/
            # seats are admin-managed data, not something a bootstrap script
            # should ever silently reset back to placeholders on a rerun.
            if not track.cohorts.exists():
                Cohort.objects.create(
                    track=track,
                    start_date=today + datetime.timedelta(days=21),
                    end_date=today + datetime.timedelta(days=21 + 56),
                    price_naira=150000,  # PLACEHOLDER — replace with the real per-track price
                    seat_count=25,  # PLACEHOLDER — replace with the real seat count
                )
                self.stdout.write(self.style.WARNING(f"  -> placeholder cohort created for {track.name}, replace price/dates/seats in the admin"))

        # Left at 0 deliberately — these render as real trust stats on the
        # homepage, so they should never ship with made-up numbers. The
        # stats bar hides itself until an admin sets real values.
        SiteSettings.load()

        faqs = [
            ("How do I pay for a cohort?", "Pick a track, log in, and check out securely with Paystack. Card or bank transfer both work."),
            ("What happens if my cohort fills up?", "Join the waitlist and we'll email you the moment a seat opens for the next cohort."),
            # Paused along with the cohort WhatsApp group feature (see git history) —
            # ("How do I get into the WhatsApp group?", "The moment your payment is confirmed, you'll get the invite link by email and on-screen."),
            ("How long does a cohort run, and when does it start?", "Each cohort runs for 8 weeks. Exact start dates are shown on each track's page, right next to the price — enrollment closes a few days before the cohort starts."),
            ("How much time do I need to commit each week?", "Roughly 6-10 hours a week, a mix of live sessions with your cohort and self-paced lessons on your dashboard that you work through between them."),
            ("Do I get a certificate?", "Yes. Every track ends with a certificate of completion, on top of a real project you shipped that you can put straight into your portfolio."),
            ("What exactly do I get for ₦5,000?", "The full project-based curriculum for your track, lesson access on your dashboard the moment payment clears, and a cohort of people learning the same track on the same timeline."),
            ("Do I need prior experience to join a track?", "No. Each track starts from the fundamentals and builds up from there. You just need to be ready to put in the work."),
            ("Do I need my own laptop?", "Yes, you'll need a laptop capable of running the tools for your track. We'll share the specific requirements once you're enrolled."),
            ("What's your refund policy?", "Check our Terms of Service page for the full refund policy."),
            ("Is the marketplace open to everyone?", "Yes, anyone can browse and buy. Selling requires an approved seller account, open to students and outside sellers alike."),
        ]
        for question, answer in faqs:
            faq, created = FAQ.objects.update_or_create(question=question, defaults={"answer": answer})
            faq_status = "created" if created else "updated"
            self.stdout.write(f"FAQ '{question[:50]}' {faq_status}")

        self.stdout.write(self.style.SUCCESS("Seed data ready. Replace placeholder prices/dates/seats in the admin before launch."))