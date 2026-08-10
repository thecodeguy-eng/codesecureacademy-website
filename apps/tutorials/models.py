from django.db import models
from django.urls import reverse


class Category(models.Model):
    """A career-path grouping shown on the tutorials home page (Frontend,
    Backend, Cybersecurity, App Development, Game Development, ...). Purely
    a free-content taxonomy — unrelated to `cohorts.Track`, which is the
    fixed 4-choice paid-bootcamp enum and stays untouched by this."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True, help_text="A short emoji shown on the category card, e.g. 🖥️")
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tutorials:subject_list", args=[self.slug])


class Subject(models.Model):
    """A free, always-public tutorial subject (HTML, CSS, JavaScript,
    Python, ...). Unlike `cohorts.Track`, this has no cohort/enrollment
    concept at all — every Article under it is readable by anyone."""

    class EditorLanguage(models.TextChoices):
        HTML = "html", "HTML"
        CSS = "css", "CSS"
        JS = "js", "JavaScript"
        PYTHON = "python", "Python"
        PHP = "php", "PHP"
        SQL = "sql", "SQL"
        JAVA = "java", "Java"
        C = "c", "C"
        CPP = "cpp", "C++"
        CSHARP = "csharp", "C#"
        DART = "dart", "Dart"
        FLUTTER = "flutter", "Flutter"
        DJANGO = "django", "Django"
        REACT = "react", "React"
        NEXTJS = "nextjs", "Next.js"
        LARAVEL = "laravel", "Laravel"
        FLASK = "flask", "Flask"
        LINUX = "linux", "Linux / Shell"
        KOTLIN = "kotlin", "Kotlin"
        SWIFT = "swift", "Swift"
        NONE = "none", "No live editor"

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="subjects"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=10, blank=True, help_text="A short emoji shown on the subject card, e.g. 🌐")
    description = models.TextField(blank=True)
    editor_language = models.CharField(
        max_length=10,
        choices=EditorLanguage.choices,
        default=EditorLanguage.NONE,
        help_text="html/css/js get a live editable preview. Everything else gets a "
        "read-only example + a pre-written expected output.",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("tutorials:article_list", args=[self.category.slug, self.slug])

    @property
    def has_live_preview(self):
        return self.editor_language in (self.EditorLanguage.HTML, self.EditorLanguage.CSS, self.EditorLanguage.JS)


class Article(models.Model):
    """A single free-to-read tutorial page under a Subject. No gating —
    the whole point of this app is content nobody has to pay to read."""

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="articles")
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    order = models.PositiveIntegerField(default=0)
    summary = models.CharField(max_length=300, blank=True)
    body = models.TextField(help_text="Article content — basic HTML allowed (headings, paragraphs, lists).")
    example_code = models.TextField(
        blank=True,
        help_text="For html/css/js subjects: a full HTML document (the editor seeds this and "
        "renders it live). For other subjects: a read-only example snippet.",
    )
    expected_output = models.TextField(
        blank=True, help_text="Only shown for subjects without a live preview — the example's expected output."
    )

    class Meta:
        ordering = ["subject", "order"]
        constraints = [
            models.UniqueConstraint(fields=["subject", "slug"], name="unique_article_slug_per_subject"),
        ]

    def __str__(self):
        return f"{self.subject.name}: {self.title}"

    def get_absolute_url(self):
        return reverse("tutorials:article_detail", args=[self.subject.category.slug, self.subject.slug, self.slug])
