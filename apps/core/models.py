from django.db import models


class SiteSettings(models.Model):
    """Singleton-style model (always use pk=1) for editable homepage copy
    — stats bar, etc. — without needing a code deploy for every tweak."""

    students_trained = models.PositiveIntegerField(default=0)
    cohorts_run = models.PositiveIntegerField(default=0)
    hiring_partners = models.PositiveIntegerField(default=0)
    last_deadline_reminder_sent_at = models.DateTimeField(
        null=True, blank=True,
        help_text="When the enrollment-reminder campaign last sent an email. "
        "Set automatically — the campaign re-sends itself on its own schedule until the deadline passes.",
    )
    last_deadline_reminder_variant = models.SmallIntegerField(
        default=-1,
        help_text="Index of the last reminder variant sent, so the next automatic send rotates to a "
        "different one instead of repeating the same email every time.",
    )
    reminder_campaign_started_at = models.DateTimeField(
        null=True, blank=True,
        help_text="When the current bounded reminder push (N sends/day for N days) began. "
        "Cleared once the push finishes its full run — set again to start a new bounded push.",
    )
    reminder_campaign_sends_done = models.PositiveSmallIntegerField(
        default=0,
        help_text="How many sends of the current bounded push have gone out so far.",
    )

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # singleton — never actually delete this row

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Site settings"


class WaitlistSignup(models.Model):
    """General 'notify me' email capture — not tied to a Track or a site
    User account, unlike `cohorts.Waitlist` which requires both. This is
    what the homepage waitlist form writes to, and what a launch-announce
    broadcast email goes out to."""

    email = models.EmailField(unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-joined_at"]

    def __str__(self):
        return self.email


class ReminderQueueItem(models.Model):
    """One recipient still waiting for the current day's reminder-campaign
    email. Populated all at once when a new day's send becomes due, then
    drained a small chunk at a time on each external cron ping (see
    apps.core.services.send_deadline_reminder_if_due) — sending the full
    list synchronously inside one request reliably exceeds the platform's
    request timeout, so the batch is spread across several pings instead."""

    email = models.EmailField()
    variant_index = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class EmailOptOut(models.Model):
    """Anyone who's clicked "unsubscribe" on a marketing/reminder email —
    checked before every recurring send (the deadline reminder campaign),
    never applied to one-off transactional email (receipts, password
    resets, etc.), which don't carry an unsubscribe link at all."""

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
