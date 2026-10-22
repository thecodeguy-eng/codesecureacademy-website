from django.conf import settings
from django.db import models
from django.utils import timezone


class Instructor(models.Model):
    """A cohort tutor — distinct from courses.Tutor, which is an
    independent seller on the self-paced Courses marketplace with its
    own Paystack payout flow. This is academy staff who teach live
    cohorts, assigned per Cohort (not per Track, since the same track
    can run with a different tutor next time)."""

    name = models.CharField(max_length=150)
    email = models.EmailField(help_text="Their login email — also where admin notices go.")
    bio = models.TextField(blank=True, help_text="Optional, shown on their tutor profile if/when we add one.")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="instructor_profile",
        help_text="Their login for the tutor dashboard — created automatically when this tutor is added.",
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class SchemeTopic(models.Model):
    """One line item in a track's scheme of work — the official
    curriculum, reused by every cohort of that track. Order is explicit
    (not created_at) so admin can reorder the syllabus without having
    to re-create rows."""

    track = models.ForeignKey("cohorts.Track", on_delete=models.CASCADE, related_name="scheme_topics")
    order = models.PositiveIntegerField(default=0)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["track", "order"]

    def __str__(self):
        return f"{self.track.name} · {self.order}. {self.title}"


class TopicProgress(models.Model):
    """Marks one SchemeTopic as covered in one specific Cohort run.
    Existence = covered; there's deliberately no row for an uncovered
    topic, so nothing needs pre-seeding when a topic or cohort is
    created — the dashboard just treats "no row" as not-yet-covered."""

    cohort = models.ForeignKey("cohorts.Cohort", on_delete=models.CASCADE, related_name="topic_progress")
    topic = models.ForeignKey(SchemeTopic, on_delete=models.CASCADE, related_name="progress")
    covered_by = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True, related_name="covered_topics")
    covered_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["cohort", "topic"], name="one_progress_row_per_cohort_topic")
        ]

    def __str__(self):
        return f"{self.cohort} covered {self.topic.title}"
