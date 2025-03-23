from django.contrib import admin
from django.utils.html import format_html  # Для отображения изображений в админке
from .models import Prediction, Comment, ImageUpload


class PredictionAdmin(admin.ModelAdmin):
    list_display = ("text", "tag", "likes", "created_at", "display_image", "display_avatar")
    list_filter = ("tag", "created_at")  # Добавляем фильтр по дате создания
    search_fields = ("text", "tag")  # Поиск по тексту и тегу
    ordering = ("-created_at",)  # Сортировка по дате создания (новые сверху)
    readonly_fields = ("display_image", "display_avatar")  # Поля только для чтения

    # Функция для отображения изображения
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"

    display_image.short_description = "Image Preview"  # Название колонки в админке

    # Функция для отображения аватара
    def display_avatar(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" />', obj.avatar.url)
        return "No avatar"

    display_avatar.short_description = "Avatar Preview"  # Название колонки в админке


class CommentAdmin(admin.ModelAdmin):
    list_display = ("username", "prediction", "text", "created_at")  # Добавляем текст комментария
    list_filter = ("created_at", "prediction")  # Фильтр по дате и предсказанию
    search_fields = ("username", "text")  # Поиск по имени пользователя и тексту
    ordering = ("-created_at",)  # Сортировка по дате создания (новые сверху)


class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("name", "tag", "display_image", "uploaded_at")  # Добавляем имя и тег
    list_filter = ("tag", "uploaded_at")  # Фильтр по тегу и дате загрузки
    search_fields = ("name", "tag")  # Поиск по имени и тегу
    ordering = ("-uploaded_at",)  # Сортировка по дате загрузки (новые сверху)
    readonly_fields = ("display_image",)  # Поле только для чтения

    # Функция для отображения изображения
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"

    display_image.short_description = "Image Preview"  # Название колонки в админке


# Регистрация моделей с улучшенными настройками админки
admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ImageUpload, ImageUploadAdmin)