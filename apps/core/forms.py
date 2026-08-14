from django import forms

from .models import WaitlistSignup


class WaitlistSignupForm(forms.ModelForm):
    class Meta:
        model = WaitlistSignup
        fields = ["email"]
        widgets = {
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "required": True}),
        }
