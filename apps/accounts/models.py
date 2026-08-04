from django.contrib.auth.models import AbstractUser
from django.db import models


class TrackChoice(models.TextChoices):
    """Mirrors apps.cohorts.models.Track's slugs. Kept as a plain choices
    enum here (not a FK) since this only records a signup-time interest,
    not a binding relationship to a real Track row."""

    FRONTEND = "frontend", "Frontend Development"
    BACKEND = "backend", "Backend Development"
    CYBERSECURITY = "cybersecurity", "Cybersecurity"
    GRAPHIC_DESIGN = "graphic_design", "Graphic Design"


class User(AbstractUser):
    """Custom user so we can carry the extra signup fields CSA asked for
    (phone number, track of interest) without bolting a separate profile
    model onto every query."""

    phone_number = models.CharField(max_length=20, blank=True)
    track_of_interest = models.CharField(
        max_length=20, choices=TrackChoice.choices, blank=True,
        help_text="What the student said they were interested in at signup — not a binding enrollment.",
    )

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def is_email_verified(self):
        return self.emailaddress_set.filter(verified=True).exists()

    @property
    def is_approved_seller(self):
        return hasattr(self, "seller_profile") and self.seller_profile.status == "approved"
