from django.conf import settings
from django.db import models
from django.urls import reverse


class Lesson(models.Model):
    """Post-enrollment curriculum content — distinct from `apps.tutorials`
    (free, public, top-of-funnel) and `apps.courses` (separately-sold
    tutor courses). This is what a student who's already paid for a track
    actually gets to learn from on the site, instead of just a WhatsApp
    link and a receipt."""

    track = models.ForeignKey("cohorts.Track", on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text="Lesson content. Basic HTML is fine (headings, lists, code blocks).")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["track", "order"]
        unique_together = ("track", "slug")

    def __str__(self):
        return f"{self.track.name}: {self.title}"

    def get_absolute_url(self):
        return reverse("lessons:lesson_detail", args=[self.track.slug, self.slug])

    def is_readable_by(self, user):
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
        unique_together = ("student", "lesson")

    def __str__(self):
        return f"{self.student} completed {self.lesson}"
