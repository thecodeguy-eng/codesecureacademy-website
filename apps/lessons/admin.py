from django.contrib import admin

from .models import Lesson, LessonProgress


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("track", "order", "title", "slug")
    list_filter = ("track",)
    list_editable = ("order",)
    search_fields = ("title", "summary")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "lesson", "completed_at")
    list_filter = ("lesson__track",)
    search_fields = ("student__email",)

    def has_add_permission(self, request):
        return False
