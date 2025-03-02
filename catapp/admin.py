from django.contrib import admin
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
    list_display = ("image", "uploaded_at")


admin.site.register(Prediction, PredictionAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ImageUpload, ImageUploadAdmin)
