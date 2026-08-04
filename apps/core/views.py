from django.shortcuts import render

from apps.cohorts.models import Track
from apps.reviews.models import Review

from .models import FAQ


def home(request):
    tracks = Track.objects.filter(is_active=True)
    reviews = Review.objects.filter(status=Review.Status.APPROVED).select_related("reviewer")[:6]
    faqs = FAQ.objects.all()[:5]
    return render(request, "core/home.html", {"tracks": tracks, "reviews": reviews, "faqs": faqs})


def about(request):
    return render(request, "core/about.html")


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, "core/faq.html", {"faqs": faqs})


def contact(request):
    return render(request, "core/contact.html")


def privacy_policy(request):
    return render(request, "core/privacy.html")


def terms_of_service(request):
    return render(request, "core/terms.html")


def cookie_policy(request):
    return render(request, "core/cookies.html")


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
