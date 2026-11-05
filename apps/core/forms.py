from django import forms

from .models import WaitlistSignup
from .services import BLAST_AUDIENCE_CHOICES


class WaitlistSignupForm(forms.ModelForm):
    class Meta:
        model = WaitlistSignup
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
        }


class BlastEmailForm(forms.Form):
    campaign_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"list": "campaign-options", "autocomplete": "off"}),
        help_text="A short label for this email (e.g. \"Nov update\"). Pick an existing one from the "
        "dropdown to resume it exactly — typing a new name always starts a fresh campaign.",
    )
    audience = forms.ChoiceField(choices=BLAST_AUDIENCE_CHOICES, initial="both")
    limit = forms.IntegerField(
        required=False, min_value=1,
        help_text="How many to send to right now. Leave blank to send to everyone left for this campaign.",
    )
    subject = forms.CharField(max_length=200)
    cta_label = forms.CharField(max_length=60, required=False, help_text="Button text. Optional.")
    cta_url = forms.URLField(required=False, help_text="Where the button links to. Optional.")
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 14}),
        help_text="Leave a blank line between paragraphs. Can be as long as you like.",
    )

    def clean_body(self):
        import re

        blocks = re.split(r"\n\s*\n", self.cleaned_data["body"].strip())
        paragraphs = [b.strip() for b in blocks if b.strip()]
        if not paragraphs:
            raise forms.ValidationError("Write something in the body.")
        return paragraphs
