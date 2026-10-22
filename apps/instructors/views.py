from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from apps.cohorts.models import Enrollment

from .models import Attendance, Session, SchemeTopic, TopicProgress


def _get_instructor_or_404(request):
    instructor = getattr(request.user, "instructor_profile", None)
    if instructor is None:
        raise Http404
    return instructor


@login_required
def instructor_dashboard(request):
    instructor = _get_instructor_or_404(request)

    cohorts = (
        instructor.cohorts.select_related("track")
        .prefetch_related("enrollments__student", "sessions__attendance")
        .order_by("-start_date")
    )

    now = timezone.now()
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

        sessions = cohort.sessions.all()
        session_rows = []
        for session in sessions:
            present_ids = set(session.attendance.values_list("student_id", flat=True))
            session_rows.append({
                "session": session,
                "roster": [{"enrollment": e, "present": e.student_id in present_ids} for e in students],
                "present_count": len(present_ids),
            })
        next_session = sessions.filter(starts_at__gte=now).first()

        cohort_data.append({
            "cohort": cohort,
            "students": students,
            "topic_rows": topic_rows,
            "covered_count": len(covered_ids),
            "total_count": len(topic_rows),
            "session_rows": session_rows,
            "next_session": next_session,
        })

    return render(request, "instructors/dashboard.html", {"instructor": instructor, "cohort_data": cohort_data})


@login_required
def toggle_topic(request, cohort_id, topic_id):
    instructor = _get_instructor_or_404(request)
    cohort = get_object_or_404(instructor.cohorts, id=cohort_id)
    topic = get_object_or_404(SchemeTopic, id=topic_id, track=cohort.track)

    if request.method == "POST":
        existing = TopicProgress.objects.filter(cohort=cohort, topic=topic).first()
        if existing:
            existing.delete()
        else:
            TopicProgress.objects.create(cohort=cohort, topic=topic, covered_by=instructor)

    return redirect("instructors:dashboard")


@login_required
def update_announcement(request, cohort_id):
    instructor = _get_instructor_or_404(request)
    cohort = get_object_or_404(instructor.cohorts, id=cohort_id)

    if request.method == "POST":
        cohort.announcement = request.POST.get("announcement", "").strip()
        cohort.announcement_updated_at = timezone.now()
        cohort.save(update_fields=["announcement", "announcement_updated_at"])

    return redirect("instructors:dashboard")


@login_required
def create_session(request, cohort_id):
    instructor = _get_instructor_or_404(request)
    cohort = get_object_or_404(instructor.cohorts, id=cohort_id)

    if request.method == "POST":
        label = request.POST.get("label", "").strip()
        dt = parse_datetime(request.POST.get("starts_at", ""))
        if dt:
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            Session.objects.create(cohort=cohort, starts_at=dt, label=label)

    return redirect("instructors:dashboard")


@login_required
def toggle_attendance(request, session_id, student_id):
    instructor = _get_instructor_or_404(request)
    session = get_object_or_404(Session, id=session_id, cohort__in=instructor.cohorts.all())

    if request.method == "POST":
        existing = Attendance.objects.filter(session=session, student_id=student_id).first()
        if existing:
            existing.delete()
        else:
            # Only mark attendance for someone actually confirmed in this cohort.
            is_enrolled = Enrollment.objects.filter(
                cohort=session.cohort, student_id=student_id, status=Enrollment.Status.CONFIRMED
            ).exists()
            if is_enrolled:
                Attendance.objects.create(session=session, student_id=student_id)

    return redirect("instructors:dashboard")
