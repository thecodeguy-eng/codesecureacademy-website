from django.db import migrations


def fix_site_domain(apps, schema_editor):
    """django.contrib.sites seeds Site(pk=1) as domain='example.com' — left
    untouched, every allauth email (password reset, email verification)
    renders with 'example.com' in the subject/body instead of the real
    site. SITE_ID=1 in settings.py, and ALLOWED_HOSTS/CSRF_TRUSTED_ORIGINS/
    DEFAULT_FROM_EMAIL already assume codesecureacademy.com as the real
    domain, so this makes the Sites framework agree with the rest of the
    project instead of shipping the Django default forever."""
    Site = apps.get_model("sites", "Site")
    Site.objects.update_or_create(
        id=1,
        defaults={"domain": "codesecureacademy.com", "name": "Code Secure Academy"},
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RunPython(fix_site_domain, noop),
    ]
