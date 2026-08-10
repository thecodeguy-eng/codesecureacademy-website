from django.db import migrations

CATEGORIES = [
    {
        "slug": "frontend",
        "name": "Frontend Development",
        "icon": "\U0001F5A5️",
        "description": "Building what users see and interact with in the browser.",
        "order": 1,
    },
    {
        "slug": "backend",
        "name": "Backend Development",
        "icon": "\U0001F5C4️",
        "description": "Servers, databases, and the logic behind the scenes.",
        "order": 2,
    },
    {
        "slug": "cybersecurity",
        "name": "Cybersecurity",
        "icon": "\U0001F512",
        "description": "Defending systems, networks, and data from attackers.",
        "order": 3,
    },
    {
        "slug": "app-development",
        "name": "App Development",
        "icon": "\U0001F4F1",
        "description": "Building native and cross-platform mobile apps.",
        "order": 4,
    },
    {
        "slug": "game-development",
        "name": "Game Development",
        "icon": "\U0001F3AE",
        "description": "The languages behind today's biggest game engines.",
        "order": 5,
    },
]

# Existing Subject slug -> Category slug
SUBJECT_CATEGORY = {
    "html": "frontend",
    "css": "frontend",
    "javascript": "frontend",
    "php": "backend",
    "python": "backend",
    "sql": "backend",
    "java": "backend",
    "django": "backend",
    "dart": "app-development",
    "flutter": "app-development",
    "cpp": "game-development",
    "csharp": "game-development",
}


def backfill_categories(apps, schema_editor):
    Category = apps.get_model("tutorials", "Category")
    Subject = apps.get_model("tutorials", "Subject")

    categories = {}
    for data in CATEGORIES:
        category, _ = Category.objects.update_or_create(
            slug=data["slug"],
            defaults={
                "name": data["name"],
                "icon": data["icon"],
                "description": data["description"],
                "order": data["order"],
                "is_active": True,
            },
        )
        categories[data["slug"]] = category

    for subject_slug, category_slug in SUBJECT_CATEGORY.items():
        Subject.objects.filter(slug=subject_slug).update(category=categories[category_slug])


def unbackfill_categories(apps, schema_editor):
    Subject = apps.get_model("tutorials", "Subject")
    Subject.objects.filter(slug__in=SUBJECT_CATEGORY.keys()).update(category=None)
    Category = apps.get_model("tutorials", "Category")
    Category.objects.filter(slug__in=[c["slug"] for c in CATEGORIES]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tutorials", "0016_category_subject_category"),
    ]

    operations = [
        migrations.RunPython(backfill_categories, unbackfill_categories),
    ]
