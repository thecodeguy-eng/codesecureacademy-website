from django.db import migrations


def fix_ampersands(apps, schema_editor):
    """Earlier seed migrations wrote HTML-entity '&amp;'/'&ndash;' into
    title/name fields that templates render WITHOUT the |safe filter (only
    `body` is safe-rendered) — so Django's auto-escaping turned '&amp;' into
    the literal text '&amp;amp;' on the page. Source migrations are fixed;
    this repairs rows already written to the database by them."""
    Category = apps.get_model("tutorials", "Category")
    Subject = apps.get_model("tutorials", "Subject")
    Article = apps.get_model("tutorials", "Article")

    for model, fields in ((Category, ["name"]), (Subject, ["name"]), (Article, ["title", "summary"])):
        for obj in model.objects.all():
            changed = False
            for field in fields:
                value = getattr(obj, field)
                if value and ("&amp;" in value or "&ndash;" in value):
                    setattr(obj, field, value.replace("&amp;", "&").replace("&ndash;", "-"))
                    changed = True
            if changed:
                obj.save(update_fields=fields)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0024_seed_linux_subject"),
    ]

    operations = [
        migrations.RunPython(fix_ampersands, noop),
    ]
