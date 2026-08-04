from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "body"]
        widgets = {
            "rating": forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            "body": forms.Textarea(attrs={"rows": 4, "placeholder": "How was it?"}),
        }
