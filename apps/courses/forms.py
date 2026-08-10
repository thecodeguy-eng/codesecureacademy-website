from django import forms

from .models import Course, CourseModule, Tutor


class TutorApplicationForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ["full_name", "phone_number", "bio", "bank_code", "account_number"]
        widgets = {
            "phone_number": forms.TextInput(attrs={"placeholder": "e.g. 080XXXXXXXX"}),
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "What will you teach?"}),
            "bank_code": forms.TextInput(attrs={"placeholder": "e.g. 058 for GTBank"}),
            "account_number": forms.TextInput(attrs={"placeholder": "10-digit NUBAN"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # bank_code/account_number are `blank=True` on the model (so admins can still
        # edit a Tutor with incomplete payout details), but an application can't be
        # submitted without them — a tutor with no payout account can never be paid.
        for field in ("phone_number", "bank_code", "account_number"):
            self.fields[field].required = True


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "slug", "description", "price_naira", "cover_image", "related_subject"]


class CourseModuleForm(forms.ModelForm):
    class Meta:
        model = CourseModule
        fields = ["title", "order", "video_url", "is_preview"]
        help_texts = {
            "video_url": "Paste your Cloudinary video URL (or a YouTube/Drive share link).",
        }
