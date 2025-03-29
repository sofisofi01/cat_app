from django.contrib import admin
from django.utils.html import format_html
from .models import Prediction, Comment, ImageUpload
from django.contrib.admin import DateFieldListFilter, RelatedFieldListFilter

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_preview', 'tag', 'likes', 'created_at', 'image_preview')
    list_filter = (
        'tag',
        ('created_at', DateFieldListFilter),
    )
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
    text_preview.short_description = 'Текст'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" style="max-height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью изображения'

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" style="border-radius: 50%;" />', obj.avatar.url)
        return "-"
    avatar_preview.short_description = 'Аватар'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'text_preview', 'prediction_link', 'created_at')
    list_filter = (
        ('created_at', DateFieldListFilter),
        ('prediction__tag', RelatedFieldListFilter),
    )
    search_fields = ('username', 'text', 'prediction__text')
    raw_id_fields = ('prediction',)
    list_per_page = 30
    date_hierarchy = 'created_at'

    def text_preview(self, obj):
        return obj.text[:100] + '...' if obj.text else '-'
    text_preview.short_description = 'Текст комментария'

    def prediction_link(self, obj):
        if obj.prediction:
            return format_html(
                '<a href="/admin/catapp/prediction/{}/change/">{}</a>',
                obj.prediction.id,
                obj.prediction.text[:50] + '...' if obj.prediction.text else f'Предсказание #{obj.prediction.id}'
            )
        return "-"
    prediction_link.short_description = 'Связанное предсказание'

@admin.register(ImageUpload)
class ImageUploadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tag', 'uploaded_at', 'image_preview')
    list_filter = (
        'tag',
        ('uploaded_at', DateFieldListFilter),
    )
    search_fields = ('name', 'tag')
    readonly_fields = ('image_preview',)
    list_per_page = 20
    date_hierarchy = 'uploaded_at'

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="max-height: 150px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Превью'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related()