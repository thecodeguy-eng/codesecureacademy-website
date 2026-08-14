from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.core.sitemaps import sitemaps

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("dashboard/", include("apps.accounts.dashboard_urls")),
    path("tracks/", include("apps.cohorts.urls")),
    path("pay/", include("apps.payments.urls")),
    path("marketplace/", include("apps.marketplace.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("tutorials/", include("apps.tutorials.urls")),
    path("courses/", include("apps.courses.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("", include("apps.core.urls")),
]

handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"
