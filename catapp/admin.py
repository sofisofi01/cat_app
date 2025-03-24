from django.contrib import admin
from .models import Prediction, Comment, ImageUpload

# Настройка админки для модели Prediction
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "tag", "likes", "created_at", "image_tag")  # Отображаемые поля
    list_filter = ("tag", "created_at")  # Фильтры
    search_fields = ("text", "tag")  # Поиск по полям
    readonly_fields = ("image_tag",)  # Поле только для чтения (изображение)

    # Метод для отображения изображения
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" height="auto" />'
        return "No Image"

    image_tag.short_description = "Image Preview"  # Название колонки
    image_tag.allow_tags = True  # Разрешить HTML-теги

# Настройка админки для модели Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "text", "prediction", "created_at")  # Отображаемые поля
    list_filter = ("prediction", "created_at")  # Фильтры
    search_fields = ("username", "text")  # Поиск по полям

# Настройка админки для модели ImageUpload
@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "tag", "uploaded_at", "image_tag")  # Отображаемые поля
    list_filter = ("tag", "uploaded_at")  # Фильтры
    search_fields = ("name", "tag")  # Поиск по полям
    readonly_fields = ("image_tag",)  # Поле только для чтения (изображение)

    # Метод для отображения изображения
    def image_tag(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" height="auto" />'
        return "No Image"

    image_tag.short_description = "Image Preview"  # Название колонки
    image_tag.allow_tags = True  # Разрешить HTML-теги