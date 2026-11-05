import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from apps.core.services import BLAST_AUDIENCE_CHOICES, blast_recipients, send_blast


class Command(BaseCommand):
    help = (
        "Send a one-off announcement email to registered users and/or waitlist signups, "
        "in capped batches so it stays under Brevo's free-plan daily send limit. Write the "
        "email as a plain text file (first line 'Subject: ...', an optional "
        "'CTA: Label | https://...' line, a blank line, then the body — blank lines separate "
        "paragraphs) and run this command. Re-run the exact same command later to send the "
        "next batch; already-attempted recipients are skipped automatically. (There's also a "
        "staff dashboard page at /insights/blast/ that does the same thing without a file.)"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "blast_key",
            help="Short, unique name for this blast (e.g. 'nov-update'). Reuse it on re-runs to resume the same send.",
        )
        parser.add_argument("content_file", help="Path to the plain text file containing Subject/CTA/body.")
        parser.add_argument("--batch-size", type=int, default=250, help="Max emails to send this run (default 250).")
        parser.add_argument(
            "--audience", default="both", choices=[key for key, _ in BLAST_AUDIENCE_CHOICES],
            help="Who to queue on the first run for this blast_key (default: both registered users and waitlist).",
        )
        parser.add_argument(
            "--dry-run", action="store_true", help="Show who the next batch would go to, without sending anything.",
        )

    def handle(self, *args, **options):
        blast_key = options["blast_key"]
        path = Path(options["content_file"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        subject, cta_label, cta_url, paragraphs = self._parse_content(path.read_text(encoding="utf-8"))

        if options["dry_run"]:
            preview = blast_recipients(options["audience"])
            self.stdout.write(f"Subject: {subject}")
            self.stdout.write(f"Audience '{options['audience']}' resolves to {len(preview)} recipient(s). First few:")
            for email in preview[:10]:
                self.stdout.write(f"  {email}")
            if len(preview) > 10:
                self.stdout.write(f"  ... and {len(preview) - 10} more")
            return

        result = send_blast(
            blast_key, subject, paragraphs, cta_label=cta_label, cta_url=cta_url,
            audience=options["audience"], batch_size=options["batch_size"],
        )
        self.stdout.write(self.style.SUCCESS(f"Sent {result['sent']}, {result['failed']} failed, this run."))
        if result["remaining"] > 0:
            self.stdout.write(
                f"{result['remaining']} recipients left — run the exact same command again "
                f"(python manage.py send_blast {blast_key} {path}) to send the next batch."
            )
        else:
            self.stdout.write(self.style.SUCCESS("That was everyone — blast complete."))

    def _parse_content(self, text):
        lines = text.splitlines()
        i = 0
        while i < len(lines) and not lines[i].strip():
            i += 1

        if i >= len(lines) or not lines[i].lower().startswith("subject:"):
            raise CommandError("Content file must start with 'Subject: ...' on its first (non-blank) line.")
        subject = lines[i].split(":", 1)[1].strip()
        i += 1

        cta_label, cta_url = None, None
        if i < len(lines) and lines[i].lower().startswith("cta:"):
            cta_raw = lines[i].split(":", 1)[1].strip()
            if "|" in cta_raw:
                cta_label, cta_url = (p.strip() for p in cta_raw.split("|", 1))
            i += 1

        body_text = "\n".join(lines[i:]).strip()
        blocks = re.split(r"\n\s*\n", body_text)
        paragraphs = [block.strip() for block in blocks if block.strip()]
        if not paragraphs:
            raise CommandError("Content file has no body text after the Subject/CTA header lines.")
        return subject, cta_label, cta_url, paragraphs
