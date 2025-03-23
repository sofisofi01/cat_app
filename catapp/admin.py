from django.contrib import admin
from django.utils.html import format_html
from .models import Prediction, Comment, ImageUpload


class PredictionAdmin(admin.ModelAdmin):
    list_display = ("text", "tag", "likes", "created_at")
    list_filter = ("tag",)
    search_fields = ("text",)
    ordering = ("-created_at",)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "prediction", "created_at")
    search_fields = ("username", "text")


class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "display_image", "uploaded_at")  # Добавляем name и tag
    list_filter = ("tag", "uploaded_at")  # Фильтр по tag и uploaded_at
    search_fields = ("name", "tag")  # Поиск по name и tag
    ordering = ("-uploaded_at",)  # Сортировка по uploaded_at
    readonly_fields = ("display_image",)  # Поле только для чтения

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"

    display_image.short_description = "Image Preview"  # Название колонки в админке


# Регистрация моделей в админке
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ImageUpload, ImageUploadAdmin)