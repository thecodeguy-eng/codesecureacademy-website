from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Track(models.Model):
    SLUG_CHOICES = [
        ("frontend", "Frontend Development"),
        ("backend", "Backend Development"),
        ("cybersecurity", "Cybersecurity"),
        ("graphic_design", "Graphic Design"),
    ]

    slug = models.SlugField(unique=True, choices=SLUG_CHOICES)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    intro_video_url = models.URLField(
        blank=True,
        help_text="YouTube (unlisted) link, Google Drive share link, or a Cloudinary-hosted video URL.",
    )
    cover_image = models.ImageField(
        upload_to="tracks/", blank=True, null=True,
        help_text="Uploaded via Cloudinary. Takes priority over Cover image URL below if both are set.",
    )
    cover_image_url = models.URLField(
        blank=True,
        help_text="A hotlinked image URL (e.g. a properly-licensed Unsplash photo) — used until a real "
        "uploaded photo replaces it. Attribution isn't required by the Unsplash License but is good practice.",
    )
    highlights = models.TextField(
        blank=True,
        help_text="What students will learn/build — one point per line. Shown as a bullet list on the track page.",
    )
    why_join = models.TextField(
        blank=True,
        help_text="Short, punchy reasons to register for this specific track — one per line. "
        "Shown as the scroll-driven 'why register' story section on the track page.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def highlight_list(self):
        return [line.strip() for line in self.highlights.splitlines() if line.strip()]

    @property
    def display_cover_image(self):
        """Prefer a real uploaded photo (Cloudinary) once one exists; fall
        back to the hotlinked URL so templates don't need an if/elif chain
        wherever a track's cover image is shown."""
        if self.cover_image:
            from apps.core.utils import cloudinary_optimized_url

            return cloudinary_optimized_url(self.cover_image.url)
        return self.cover_image_url

    @property
    def why_join_list(self):
        return [line.strip() for line in self.why_join.splitlines() if line.strip()]

    def get_absolute_url(self):
        return reverse("cohorts:track_detail", args=[self.slug])

    @property
    def is_embeddable_video(self):
        from apps.core.video import is_embeddable_video

        return is_embeddable_video(self.intro_video_url)

    @property
    def embed_video_url(self):
        from apps.core.video import embed_video_url

        return embed_video_url(self.intro_video_url)

    @property
    def open_cohort(self):
        return self.cohorts.filter(status=Cohort.Status.OPEN).order_by("start_date").first()

    @property
    def next_cohort(self):
        return self.open_cohort or self.cohorts.filter(start_date__gte=timezone.now().date()).order_by("start_date").first()


class Cohort(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        FULL = "full", "Full"
        CLOSED = "closed", "Closed"

    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="cohorts")
    start_date = models.DateField()
    end_date = models.DateField()
    enrollment_deadline = models.DateField(
        null=True, blank=True,
        help_text="Last day new enrollments are accepted for this cohort. Leave blank for no cutoff.",
    )
    price_naira = models.DecimalField(max_digits=10, decimal_places=2)
    seat_count = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return f"{self.track.name} — {self.start_date:%b %Y}"

    @property
    def seats_taken(self):
        return self.enrollments.filter(
            status__in=[Enrollment.Status.HELD, Enrollment.Status.CONFIRMED]
        ).count()

    @property
    def seats_available(self):
        return max(self.seat_count - self.seats_taken, 0)

    @property
    def is_full(self):
        return self.status != self.Status.CLOSED and self.seats_available <= 0

    @property
    def is_past_deadline(self):
        return bool(self.enrollment_deadline) and timezone.now().date() > self.enrollment_deadline

    @property
    def accepting_enrollment(self):
        """The single source of truth for whether the enroll CTA (vs.
        waitlist) should show. Distinct from `is_full` — an admin can flip
        a cohort to CLOSED to pull it out of direct enrollment even with
        seats left, which `is_full` alone doesn't capture."""
        return self.status == self.Status.OPEN and self.seats_available > 0 and not self.is_past_deadline

    def refresh_status(self):
        if self.status == self.Status.CLOSED:
            return
        new_status = self.Status.FULL if self.seats_available <= 0 else self.Status.OPEN
        if new_status != self.status:
            self.status = new_status
            self.save(update_fields=["status"])


class Enrollment(models.Model):
    class Status(models.TextChoices):
        HELD = "held", "Seat held (payment in progress)"
        CONFIRMED = "confirmed", "Confirmed"
        FAILED = "failed", "Payment failed"
        EXPIRED = "expired", "Hold expired"

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    cohort = models.ForeignKey(Cohort, on_delete=models.CASCADE, related_name="enrollments")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.HELD)
    seat_held_at = models.DateTimeField(default=timezone.now)
    grace_extended_until = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.student} -> {self.cohort} ({self.status})"

    def get_success_url(self):
        return reverse("cohorts:enrollment_success", args=[self.id])

    def mark_confirmed(self):
        if self.status == self.Status.CONFIRMED:
            return
        self.status = self.Status.CONFIRMED
        self.confirmed_at = timezone.now()
        self.save(update_fields=["status", "confirmed_at"])
        self.cohort.refresh_status()
        from apps.whatsapp.services import send_invite_for_enrollment
        from apps.cohorts.services import send_enrollment_receipt

        send_enrollment_receipt(self)
        send_invite_for_enrollment(self)


class Waitlist(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="waitlist_entries")
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name="waitlist_entries")
    joined_at = models.DateTimeField(auto_now_add=True)
    notified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "track")
        ordering = ["joined_at"]

    def __str__(self):
        return f"{self.student} waiting for {self.track}"
