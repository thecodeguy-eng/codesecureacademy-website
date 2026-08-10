from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.cohorts.models import Track

from .models import Lesson, LessonProgress


def lessons_home(request):
    tracks = Track.objects.filter(is_active=True, lessons__isnull=False).distinct()
    return render(request, "lessons/lessons_home.html", {"tracks": tracks})


def lesson_list(request, track_slug):
    track = get_object_or_404(Track, slug=track_slug, is_active=True)
    lessons = track.lessons.all()

    completed_ids = set()
    if request.user.is_authenticated:
        completed_ids = set(
            LessonProgress.objects.filter(student=request.user, lesson__track=track).values_list(
                "lesson_id", flat=True
            )
        )

    return render(
        request,
        "lessons/lesson_list.html",
        {"track": track, "lessons": lessons, "completed_ids": completed_ids},
    )


def lesson_detail(request, track_slug, lesson_slug):
    track = get_object_or_404(Track, slug=track_slug, is_active=True)
    lesson = get_object_or_404(Lesson, track=track, slug=lesson_slug)
    can_read = lesson.is_readable_by(request.user)

    completed = (
        can_read
        and request.user.is_authenticated
        and LessonProgress.objects.filter(student=request.user, lesson=lesson).exists()
    )

    ordered = list(track.lessons.all())
    index = ordered.index(lesson) if lesson in ordered else -1
    prev_lesson = ordered[index - 1] if index > 0 else None
    next_lesson = ordered[index + 1] if 0 <= index < len(ordered) - 1 else None

    return render(
        request,
        "lessons/lesson_detail.html",
        {
            "track": track,
            "lesson": lesson,
            "can_read": can_read,
            "completed": completed,
            "prev_lesson": prev_lesson,
            "next_lesson": next_lesson,
        },
    )


@login_required
def mark_complete(request, track_slug, lesson_slug):
    track = get_object_or_404(Track, slug=track_slug, is_active=True)
    lesson = get_object_or_404(Lesson, track=track, slug=lesson_slug)
    if not lesson.is_readable_by(request.user):
        messages.error(request, "Enroll in this track to mark that lesson complete.")
        return redirect(lesson.get_absolute_url())
    LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
    messages.success(request, "Marked complete.")
    return redirect(lesson.get_absolute_url())
