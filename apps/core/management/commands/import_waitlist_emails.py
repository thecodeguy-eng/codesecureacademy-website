import csv
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import validate_email
from django.utils import timezone

from apps.core.models import WaitlistSignup


class Command(BaseCommand):
    help = (
        "One-off import of the pre-launch waitlist emails exported from Brevo "
        "(semicolon-delimited EMAIL;ADDED_TIME;MODIFIED_TIME, dates as DD-MM-YYYY) "
        "into WaitlistSignup. Idempotent — safe to rerun; existing emails are left untouched."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            nargs="?",
            default=str(settings.BASE_DIR / "waitlist-emails"),
            help="Path to the exported file (default: waitlist-emails in the project root).",
        )

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {path}"))
            return

        created, skipped_existing, skipped_invalid = 0, 0, 0

        with path.open(newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            next(reader, None)  # header row
            for row in reader:
                if not row or not row[0].strip():
                    continue
                email = row[0].strip().lower()
                added_time = row[1].strip() if len(row) > 1 else ""

                try:
                    validate_email(email)
                except ValidationError:
                    skipped_invalid += 1
                    continue

                if WaitlistSignup.objects.filter(email__iexact=email).exists():
                    skipped_existing += 1
                    continue

                obj = WaitlistSignup.objects.create(email=email)

                if added_time:
                    try:
                        joined_at = timezone.make_aware(datetime.strptime(added_time, "%d-%m-%Y"))
                        WaitlistSignup.objects.filter(pk=obj.pk).update(joined_at=joined_at)
                    except ValueError:
                        pass

                created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported {created} new signups. Skipped {skipped_existing} already present, "
            f"{skipped_invalid} invalid email(s)."
        ))
