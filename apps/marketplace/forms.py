from django import forms

from .models import Listing, Seller


class SellerApplicationForm(forms.ModelForm):
    """Business details only — bank/payout info is collected afterward,
    once the application is approved (see SellerPaymentInfoForm)."""

    class Meta:
        model = Seller
        fields = ["business_name", "category", "bio"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3, "placeholder": "What do you sell / offer?"}),
        }


class SellerPaymentInfoForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ["bank_code", "account_number"]
        widgets = {
            "bank_code": forms.TextInput(attrs={"placeholder": "e.g. 058 for GTBank"}),
            "account_number": forms.TextInput(attrs={"placeholder": "10-digit NUBAN"}),
        }


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "slug", "category", "description", "price_naira", "cover_image"]
