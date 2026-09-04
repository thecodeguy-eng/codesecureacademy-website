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
