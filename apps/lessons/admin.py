from django.contrib import admin

from .models import Lesson, LessonProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "track", "order", "is_free")
    list_filter = ("track", "is_free")
    list_editable = ("order", "is_free")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "completed_at")
    list_filter = ("lesson__track",)
    search_fields = ("student__username", "student__email")
