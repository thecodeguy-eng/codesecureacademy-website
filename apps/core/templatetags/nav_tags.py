from django import template

register = template.Library()


@register.filter
def starts_with(value, prefix):
    """Used to mark the matching main-nav link active by URL prefix, e.g.
    `request.path|starts_with:"/tracks/"` so /tracks/frontend/ still
    highlights "Tracks", not just the exact /tracks/ listing page."""
    return str(value).startswith(prefix)
