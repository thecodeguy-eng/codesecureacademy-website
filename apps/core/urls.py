from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("waitlist/join/", views.join_general_waitlist, name="join_general_waitlist"),
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe"),
    path("about/", views.about, name="about"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("cookie-policy/", views.cookie_policy, name="cookie_policy"),
]
