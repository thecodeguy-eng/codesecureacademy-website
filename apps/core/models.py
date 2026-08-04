from django.db import models


class SiteSettings(models.Model):
    """Singleton-style model (always use pk=1) for editable homepage copy
    — stats bar, etc. — without needing a code deploy for every tweak."""

    students_trained = models.PositiveIntegerField(default=0)
    cohorts_run = models.PositiveIntegerField(default=0)
    hiring_partners = models.PositiveIntegerField(default=0)

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
