from django.conf import settings
from django.db import models


class AnalyticsEvent(models.Model):
    """A lightweight funnel/usage log, not a full product-analytics system —
    just enough to answer real questions (where signups drop off, which
    channel actually converts) instead of guessing. Written only through
    `apps.analytics.services.track()`, which never lets a logging failure
    break the request it's attached to."""

    name = models.CharField(max_length=60, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="analytics_events",
    )
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["name", "created_at"])]

    def __str__(self):
        return f"{self.name} @ {self.created_at:%Y-%m-%d %H:%M}"
