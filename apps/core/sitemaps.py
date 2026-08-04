from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from apps.cohorts.models import Track
from apps.marketplace.models import Listing


class StaticViewSitemap(Sitemap):
    priority = 0.6
    changefreq = "weekly"

    def items(self):
        return ["home", "about", "faq"]

    def location(self, item):
        return reverse(item)


class TrackSitemap(Sitemap):
    priority = 0.9
    changefreq = "weekly"

    def items(self):
        return Track.objects.filter(is_active=True)

    def location(self, obj):
        return obj.get_absolute_url()


class ListingSitemap(Sitemap):
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Listing.objects.filter(status=Listing.Status.ACTIVE)

    def location(self, obj):
        return obj.get_absolute_url()


sitemaps = {
    "static": StaticViewSitemap,
    "tracks": TrackSitemap,
    "marketplace": ListingSitemap,
}
