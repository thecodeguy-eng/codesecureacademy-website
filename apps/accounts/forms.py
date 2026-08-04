from allauth.account.forms import SignupForm
from django import forms
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from .models import TrackChoice


class CSASignupForm(SignupForm):
    """Extends allauth's signup form with the fields the brief asked for:
    name, phone number, and track of interest — plus a required Terms/
    Privacy acknowledgement, since we now have real policy pages to link to."""

    first_name = forms.CharField(max_length=150, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")
    phone_number = forms.CharField(max_length=20, label="Phone number")
    track_of_interest = forms.ChoiceField(
        choices=[("", "Not sure yet")] + list(TrackChoice.choices),
        required=False,
        label="Which track are you interested in?",
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        error_messages={"required": "You need to agree to the Terms and Privacy Policy to continue."},
    )

    field_order = [
        "first_name", "last_name", "email", "phone_number", "track_of_interest",
        "password1", "password2", "agree_to_terms",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["agree_to_terms"].label = mark_safe(
            'I agree to the <a href="%s" target="_blank">Terms of Service</a> and '
            '<a href="%s" target="_blank">Privacy Policy</a>'
            % (reverse_lazy("terms_of_service"), reverse_lazy("privacy_policy"))
        )

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        user.track_of_interest = self.cleaned_data["track_of_interest"]
        user.save()
        return user
