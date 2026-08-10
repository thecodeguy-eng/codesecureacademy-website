from django.shortcuts import get_object_or_404, render

from .models import Article, Category, Subject


def category_list(request):
    categories = Category.objects.filter(is_active=True)
    return render(request, "tutorials/category_list.html", {"categories": categories})


def subject_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subjects = category.subjects.filter(is_active=True)
    return render(request, "tutorials/subject_list.html", {"category": category, "subjects": subjects})


def article_list(request, category_slug, subject_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, category=category, is_active=True)
    articles = subject.articles.all()
    return render(
        request, "tutorials/article_list.html", {"category": category, "subject": subject, "articles": articles}
    )


def article_detail(request, category_slug, subject_slug, article_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subject = get_object_or_404(Subject, slug=subject_slug, category=category, is_active=True)
    article = get_object_or_404(Article, subject=subject, slug=article_slug)

    ordered = list(subject.articles.all())
    index = ordered.index(article) if article in ordered else -1
    prev_article = ordered[index - 1] if index > 0 else None
    next_article = ordered[index + 1] if 0 <= index < len(ordered) - 1 else None

    from apps.courses.models import Course

    related_courses = Course.objects.filter(related_subject=subject, status=Course.Status.ACTIVE)

    return render(
        request,
        "tutorials/article_detail.html",
        {
            "category": category,
            "subject": subject,
            "article": article,
            "prev_article": prev_article,
            "next_article": next_article,
            "related_courses": related_courses,
        },
    )
