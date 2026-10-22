from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from apps.cohorts.models import Cohort, Enrollment

from .models import SchemeTopic, TopicProgress


@login_required
def instructor_dashboard(request):
    instructor = getattr(request.user, "instructor_profile", None)
    if instructor is None:
        raise Http404

    cohorts = (
        instructor.cohorts.select_related("track")
        .prefetch_related("enrollments__student")
        .order_by("-start_date")
    )

    cohort_data = []
    for cohort in cohorts:
        students = (
            Enrollment.objects.filter(cohort=cohort, status=Enrollment.Status.CONFIRMED)
            .select_related("student")
            .order_by("student__first_name", "student__username")
        )
        topics = cohort.track.scheme_topics.all()
        covered_ids = set(
            TopicProgress.objects.filter(cohort=cohort, topic__in=topics).values_list("topic_id", flat=True)
        )
        topic_rows = [{"topic": t, "covered": t.id in covered_ids} for t in topics]
        cohort_data.append({
            "cohort": cohort,
            "students": students,
            "topic_rows": topic_rows,
            "covered_count": len(covered_ids),
            "total_count": len(topic_rows),
        })

    return render(request, "instructors/dashboard.html", {"instructor": instructor, "cohort_data": cohort_data})


@login_required
def toggle_topic(request, cohort_id, topic_id):
    instructor = getattr(request.user, "instructor_profile", None)
    if instructor is None:
        raise Http404

    cohort = get_object_or_404(instructor.cohorts, id=cohort_id)
    topic = get_object_or_404(SchemeTopic, id=topic_id, track=cohort.track)

    if request.method == "POST":
        existing = TopicProgress.objects.filter(cohort=cohort, topic=topic).first()
        if existing:
            existing.delete()
        else:
            TopicProgress.objects.create(cohort=cohort, topic=topic, covered_by=instructor)

    return redirect("instructors:dashboard")
