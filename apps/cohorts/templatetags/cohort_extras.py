from django import template

register = template.Library()

# Ordered so more specific keywords are checked before generic ones
# (e.g. "database" before a bare fallback). Matched against the lowercased
# curriculum line — admins can still edit the free-text highlight/why_join
# lines in admin without touching this mapping, it just won't get a
# specific icon if the wording changes too much (falls back to "code").
_ICON_KEYWORDS = [
    ("javascript", "javascript"),
    ("react", "react"),
    ("html", "code"),
    ("css", "css"),
    ("typography", "design"),
    ("figma", "design"),
    ("brand", "design"),
    ("layout", "design"),
    ("client-brief", "design"),
    ("django", "server"),
    ("python", "server"),
    ("server-side", "server"),
    ("database", "database"),
    ("sql", "database"),
    ("rest api", "api"),
    ("api", "api"),
    ("auth", "security"),
    ("security", "security"),
    ("owasp", "security"),
    ("vulnerabilit", "security"),
    ("incident", "security"),
    ("lab", "security"),
    ("network", "network"),
    ("git", "git"),
    ("deploy", "deploy"),
]


@register.filter
def tech_icon(text):
    lowered = (text or "").lower()
    for keyword, icon in _ICON_KEYWORDS:
        if keyword in lowered:
            return icon
    return "code"
