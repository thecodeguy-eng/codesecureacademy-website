from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.cohorts.models import Track
from apps.courses.models import Course
from apps.marketplace.models import Listing
from apps.reviews.models import Review
from apps.tutorials.models import Article

from .forms import WaitlistSignupForm
from .models import FAQ, WaitlistSignup


def home(request):
    tracks = Track.objects.filter(is_active=True)
    reviews = Review.objects.filter(status=Review.Status.APPROVED).select_related("reviewer")[:6]
    faqs = FAQ.objects.all()[:5]
    waitlist_form = WaitlistSignupForm()
    return render(
        request,
        "core/home.html",
        {"tracks": tracks, "reviews": reviews, "faqs": faqs, "waitlist_form": waitlist_form},
    )


def join_general_waitlist(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        form = WaitlistSignupForm(request.POST)
        if WaitlistSignup.objects.filter(email__iexact=email).exists():
            messages.success(request, "You're already on the waitlist — we'll email you when a track opens up.")
        elif form.is_valid():
            form.save()
            messages.success(request, "You're on the waitlist — we'll email you when a track opens up.")
        else:
            messages.error(request, "Enter a valid email address to join the waitlist.")

    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect("home")


def search(request):
    query = request.GET.get("q", "").strip()
    articles = courses = tracks = listings = []

    if query:
        articles = Article.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        ).select_related("subject", "subject__category")[:20]
        courses = Course.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            status=Course.Status.ACTIVE,
        )[:20]
        tracks = Track.objects.filter(
            Q(name__icontains=query) | Q(tagline__icontains=query) | Q(description__icontains=query),
            is_active=True,
        )[:20]
        listings = Listing.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            status=Listing.Status.ACTIVE,
        )[:20]

    return render(
        request,
        "core/search_results.html",
        {
            "query": query,
            "articles": articles,
            "courses": courses,
            "tracks": tracks,
            "listings": listings,
            "result_count": len(articles) + len(courses) + len(tracks) + len(listings),
        },
    )


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
