from django import template

from apps.cohorts.models import Track

register = template.Library()


@register.inclusion_tag("tutorials/_cta_banner.html")
def tutorial_cta_banner(category=None):
    """A quiet, always-present reminder on every free-tutorial page pointing
    back at the paid cohort it's a preview of — enroll if the matching
    track is open, join the waitlist if it isn't, or a generic nudge
    toward all tracks if this category has no matching track (e.g. App
    Development, Game Development — free-content-only categories).

    Matched by slug: tutorials.Category and cohorts.Track happen to share
    slugs for the three categories that do have a track (frontend, backend,
    cybersecurity) — see apps/tutorials/models.py's Category docstring for
    why they're otherwise unrelated taxonomies.
    """
    track = None
    if category is not None:
        track = Track.objects.filter(slug=category.slug, is_active=True).first()

    cohort = track.next_cohort if track else None
    return {"track": track, "cohort": cohort}
