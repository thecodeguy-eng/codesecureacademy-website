from django.conf import settings
from django.db import models
from django.urls import reverse


class Lesson(models.Model):
    """A single free-to-read-or-paid-gated lesson under a track. The
    free/paid split is what lets visitors try a track before enrolling —
    see `is_readable_by` for the actual access check, which the view
    enforces (a locked lesson's body must never reach an unauthorized
    response, not just be hidden in the template)."""

    track = models.ForeignKey("cohorts.Track", on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)
    is_free = models.BooleanField(
        default=True,
        help_text="Unchecked = requires a confirmed enrollment in this track to read.",
    )
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text="Lesson content — basic HTML allowed (headings, code blocks, lists).")

    class Meta:
        ordering = ["track", "order"]
        constraints = [
            models.UniqueConstraint(fields=["track", "slug"], name="unique_lesson_slug_per_track"),
        ]

    def __str__(self):
        return f"{self.track.name}: {self.title}"

    def get_absolute_url(self):
        return reverse("lessons:lesson_detail", args=[self.track.slug, self.slug])

    def is_readable_by(self, user):
        if self.is_free:
            return True
        if not user.is_authenticated:
            return False
        from apps.cohorts.models import Enrollment

        return Enrollment.objects.filter(
            student=user, cohort__track=self.track, status=Enrollment.Status.CONFIRMED
        ).exists()


class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_entries")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "lesson"], name="unique_progress_per_student_lesson"),
        ]

    def __str__(self):
        return f"{self.student} completed {self.lesson}"
