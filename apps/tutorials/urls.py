from django.urls import path

from . import views

app_name = "tutorials"

urlpatterns = [
    path("", views.category_list, name="category_list"),
    path("<slug:category_slug>/", views.subject_list, name="subject_list"),
    path("<slug:category_slug>/<slug:subject_slug>/", views.article_list, name="article_list"),
    path("<slug:category_slug>/<slug:subject_slug>/<slug:article_slug>/", views.article_detail, name="article_detail"),
]
