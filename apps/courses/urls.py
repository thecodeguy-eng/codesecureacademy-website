from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("teach/apply/", views.apply_tutor, name="apply_tutor"),
    path("teach/dashboard/", views.tutor_dashboard, name="tutor_dashboard"),
    path("teach/courses/new/", views.create_course, name="create_course"),
    path("teach/<slug:slug>/modules/new/", views.add_module, name="add_module"),
    path("teach/<slug:slug>/live-sessions/new/", views.add_live_session, name="add_live_session"),
    path("purchase/<int:purchase_id>/success/", views.purchase_success, name="purchase_success"),
    path("<slug:slug>/checkout/", views.start_checkout, name="start_checkout"),
    path("<slug:slug>/watch/<int:module_id>/", views.watch_module, name="watch_module"),
    path("<slug:slug>/", views.course_detail, name="course_detail"),
]
