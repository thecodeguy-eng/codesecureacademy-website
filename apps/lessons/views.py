from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.cohorts.models import Enrollment, Track

from .models import Lesson, LessonProgress


def _enrolled_tracks(user):
    track_ids = Enrollment.objects.filter(
        student=user, status=Enrollment.Status.CONFIRMED
    ).values_list("cohort__track_id", flat=True)
    return Track.objects.filter(id__in=set(track_ids))


@login_required
def my_learning(request):
    tracks = list(_enrolled_tracks(request.user))
    completed_ids = set(
        LessonProgress.objects.filter(student=request.user).values_list("lesson_id", flat=True)
    )
    track_progress = []
    for track in tracks:
        lessons = list(track.lessons.all())
        done = sum(1 for lesson in lessons if lesson.id in completed_ids)
        percent = round(done / len(lessons) * 100) if lessons else 0
        track_progress.append({"track": track, "total": len(lessons), "done": done, "percent": percent})

    return render(request, "lessons/my_learning.html", {"track_progress": track_progress})


@login_required
def track_lessons(request, track_slug):
    track = get_object_or_404(Track, slug=track_slug)
    if track not in _enrolled_tracks(request.user):
        messages.info(request, "Enroll in this track to unlock its lessons.")
        return redirect(track.get_absolute_url())

    lessons = track.lessons.all()
    completed_ids = set(
        LessonProgress.objects.filter(student=request.user, lesson__track=track).values_list("lesson_id", flat=True)
    )
    return render(
        request,
        "lessons/track_lessons.html",
        {"track": track, "lessons": lessons, "completed_ids": completed_ids},
    )


@login_required
def lesson_detail(request, track_slug, lesson_slug):
    track = get_object_or_404(Track, slug=track_slug)
    lesson = get_object_or_404(Lesson, track=track, slug=lesson_slug)

    if not lesson.is_readable_by(request.user):
        messages.info(request, "Enroll in this track to unlock its lessons.")
        return redirect(track.get_absolute_url())

    lessons = list(track.lessons.all())
    index = next((i for i, item in enumerate(lessons) if item.id == lesson.id), 0)
    previous_lesson = lessons[index - 1] if index > 0 else None
    next_lesson = lessons[index + 1] if index < len(lessons) - 1 else None
    is_complete = LessonProgress.objects.filter(student=request.user, lesson=lesson).exists()

    return render(
        request,
        "lessons/lesson_detail.html",
        {
            "track": track, "lesson": lesson, "is_complete": is_complete,
            "previous_lesson": previous_lesson, "next_lesson": next_lesson,
        },
    )


@login_required
def mark_lesson_complete(request, track_slug, lesson_slug):
    if request.method != "POST":
        return redirect("lessons:lesson_detail", track_slug=track_slug, lesson_slug=lesson_slug)

    track = get_object_or_404(Track, slug=track_slug)
    lesson = get_object_or_404(Lesson, track=track, slug=lesson_slug)
    if lesson.is_readable_by(request.user):
        LessonProgress.objects.get_or_create(student=request.user, lesson=lesson)
        messages.success(request, "Marked as complete.")
    return redirect("lessons:lesson_detail", track_slug=track_slug, lesson_slug=lesson_slug)
