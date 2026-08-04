from django import forms

from .models import Listing, Seller


class SellerApplicationForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ["business_name", "category", "bio", "bank_code", "account_number"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "What do you sell / offer?"}),
            "bank_code": forms.TextInput(attrs={"placeholder": "e.g. 058 for GTBank"}),
            "account_number": forms.TextInput(attrs={"placeholder": "10-digit NUBAN"}),
        }


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "slug", "category", "description", "price_naira", "cover_image"]
