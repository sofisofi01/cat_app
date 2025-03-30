from django.contrib import admin
from django.utils.html import format_html
from .models import Prediction, Comment, ImageUpload

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'tag', 'likes', 'created_at', 'image_preview')
    list_filter = ('tag', 'created_at')
    search_fields = ('text', 'tag')
    readonly_fields = ('image_preview', 'avatar_preview')
    date_hierarchy = 'created_at'
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('text', 'tag', 'likes')
        }),
        ('Media', {
            'fields': ('image', 'image_preview', 'avatar', 'avatar_preview')
        }),
    )

    def text_preview(self, obj):
        return obj.text[:50] + '...' if obj.text else '-'
    text_preview.short_description = 'Text'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = 'Avatar'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'text_preview', 'prediction_link', 'created_at')
    list_filter = ('created_at', 'prediction__tag')  # Фильтр по тегу предсказания
    search_fields = ('username', 'text', 'prediction__text')
    raw_id_fields = ('prediction',)
    list_per_page = 30
    date_hierarchy = 'created_at'

    def text_preview(self, obj):
        return obj.text[:100] + '...' if obj.text else '-'
    text_preview.short_description = 'Comment'

    def prediction_link(self, obj):
        if obj.prediction:
            return format_html('<a href="/admin/catapp/prediction/{}/change/">{}</a>', 
                             obj.prediction.id, 
                             obj.prediction.text[:50] + '...' if obj.prediction.text else f'Prediction #{obj.prediction.id}')
        return "-"
    prediction_link.short_description = 'Prediction'

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_preview', 'tag', 'uploaded_at', 'image_preview')
    list_filter = ('tag', 'uploaded_at')  # Фильтры по тегу и дате
    search_fields = ('name', 'tag')
    readonly_fields = ('image_preview',)
    list_per_page = 20
    date_hierarchy = 'uploaded_at'

    def name_preview(self, obj):
        return obj.name[:50] + '...' if obj.name else '-'
    name_preview.short_description = 'Name'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="max-height: 150px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image'