from django.db import models


class TrackWhatsAppGroup(models.Model):
    """Admin-editable invite link per track. CSA creates and maintains the
    actual WhatsApp group manually; the site just hands out the link the
    moment a payment is confirmed (email + on-screen) — the "clean" v1
    approach agreed on instead of the full WhatsApp Business API auto-add."""

    track = models.OneToOneField("cohorts.Track", on_delete=models.CASCADE, related_name="whatsapp_group")
    invite_link = models.URLField(help_text="e.g. https://chat.whatsapp.com/XXXXXXXXXXXXXXXXXXXXXX")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"WhatsApp group for {self.track}"
