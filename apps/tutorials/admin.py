from django.contrib import admin

from .models import Article, Category, Subject


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "editor_language", "order", "is_active")
    list_filter = ("category", "editor_language", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "order")
    list_filter = ("subject__category", "subject")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "summary")
