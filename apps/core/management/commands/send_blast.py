import re
from pathlib import Path

from django.core.mail import EmailMultiAlternatives, get_connection
from django.core.management.base import BaseCommand, CommandError
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape
from django.utils.safestring import mark_safe

DEFAULT_CTA_LABEL = "Visit Code Secure Academy"
DEFAULT_CTA_URL = "https://codesecureacademy.com/"


class Command(BaseCommand):
    help = (
        "Send a one-off announcement email to every registered user and waitlist signup, "
        "in capped batches so it stays under Brevo's free-plan daily send limit. Write the "
        "email as a plain text file (first line 'Subject: ...', an optional "
        "'CTA: Label | https://...' line, a blank line, then the body — blank lines separate "
        "paragraphs) and run this command. Re-run the exact same command later to send the "
        "next batch; already-attempted recipients are skipped automatically."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "blast_key",
            help="Short, unique name for this blast (e.g. 'nov-update'). Reuse it on re-runs to resume the same send.",
        )
        parser.add_argument("content_file", help="Path to the plain text file containing Subject/CTA/body.")
        parser.add_argument("--batch-size", type=int, default=250, help="Max emails to send this run (default 250).")
        parser.add_argument(
            "--dry-run", action="store_true", help="Show who the next batch would go to, without sending anything.",
        )

    def handle(self, *args, **options):
        from apps.core.models import BlastRecipient
        from apps.core.services import blast_recipients, unsubscribe_url

        blast_key = options["blast_key"]
        batch_size = options["batch_size"]
        path = Path(options["content_file"])
        if not path.exists():
            raise CommandError(f"File not found: {path}")

        subject, cta_label, cta_url, raw_paragraphs = self._parse_content(path.read_text(encoding="utf-8"))
        html_paragraphs = [mark_safe(escape(p).replace("\n", "<br>")) for p in raw_paragraphs]

        if not BlastRecipient.objects.filter(blast_key=blast_key).exists():
            emails = blast_recipients()
            BlastRecipient.objects.bulk_create(
                BlastRecipient(blast_key=blast_key, email=email, position=i) for i, email in enumerate(emails)
            )
            self.stdout.write(self.style.SUCCESS(f"Queued {len(emails)} recipients for blast '{blast_key}'."))

        pending = BlastRecipient.objects.filter(blast_key=blast_key, sent_at__isnull=True).order_by("position")
        total_remaining = pending.count()
        batch = list(pending[:batch_size])

        if not batch:
            self.stdout.write(self.style.SUCCESS(
                f"Nothing left to send for '{blast_key}' — every recipient already has an attempt logged."
            ))
            return

        if options["dry_run"]:
            self.stdout.write(f"Subject: {subject}")
            self.stdout.write(f"Would send to {len(batch)} of {total_remaining} remaining recipients this run:")
            for r in batch[:10]:
                self.stdout.write(f"  {r.email}")
            if len(batch) > 10:
                self.stdout.write(f"  ... and {len(batch) - 10} more")
            return

        connection = get_connection(fail_silently=True)
        connection.open()
        sent, failed = 0, 0
        try:
            for recipient in batch:
                html_body = render_to_string(
                    "emails/campaign_email.html",
                    {
                        "heading": subject,
                        "paragraphs": html_paragraphs,
                        "cta_url": cta_url,
                        "cta_label": cta_label,
                        "unsubscribe_url": unsubscribe_url(recipient.email),
                        "days_left_display": None,
                    },
                )
                plain_body = "\n\n".join(
                    raw_paragraphs
                    + [f"{cta_label}: {cta_url}", "Code Secure Academy", f"Unsubscribe: {unsubscribe_url(recipient.email)}"]
                )
                msg = EmailMultiAlternatives(subject, plain_body, to=[recipient.email])
                msg.attach_alternative(html_body, "text/html")
                msg.connection = connection
                ok = msg.send(fail_silently=True)
                recipient.sent_at = timezone.now()
                recipient.failed = not ok
                recipient.save(update_fields=["sent_at", "failed"])
                if ok:
                    sent += 1
                else:
                    failed += 1
        finally:
            connection.close()

        remaining_after = total_remaining - len(batch)
        self.stdout.write(self.style.SUCCESS(f"Sent {sent}, {failed} failed, this run."))
        if remaining_after > 0:
            self.stdout.write(
                f"{remaining_after} recipients left — run the exact same command again "
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

        cta_label, cta_url = DEFAULT_CTA_LABEL, DEFAULT_CTA_URL
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
