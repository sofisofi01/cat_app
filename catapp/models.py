from django.db import models

class PredictionTag(models.TextChoices):
    PHILOSOPHICAL = "philosophical", "Философское"
    FUNNY = "funny", "Смешное"
    INSPIRATIONAL = "inspirational", "Жизнеутверждающее"
    DOMESTIC = "domestic", "Домашнее"
    RELAX = "relax", "Релакс"
    DREAMS = "dreams", "Мечты"
    TRIVIAL = "trivial", "Мелочи"
    NOSTALGIA = "nostalgia", "Ностальгия"
    MYSTERIOUS = "mysterious", "Загадочное"
    FATE = "fate", "Судьба"
    EVERYDAY = "everyday", "Бытовое"

class Prediction(models.Model):
    text = models.TextField(null=True, blank=True, max_length=500)
    image = models.ImageField(upload_to="predictions/", null=True, blank=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField(
        max_length=20,
        choices=PredictionTag.choices,
        default=PredictionTag.PHILOSOPHICAL,
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    def __str__(self):
        return self.text[:50] if self.text else f"Image Prediction {self.id}"

class Comment(models.Model):
    prediction = models.ForeignKey(
        Prediction, 
        related_name="comments", 
        on_delete=models.CASCADE,
        verbose_name="Предсказание" 
    )
    username = models.CharField(max_length=100, verbose_name="Имя пользователя")
    text = models.TextField(max_length=300, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.username}"

    class Meta:
        verbose_name = "Comments"
        verbose_name_plural = "Comments"
        ordering = ['-created_at'] 

class ImageUpload(models.Model):
    image = models.ImageField(upload_to="uploads/%Y/%m/%d/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    name = models.CharField(max_length=300, verbose_name="Название")
    tag = models.CharField(
        max_length=20,
        choices=PredictionTag.choices,
        default=PredictionTag.PHILOSOPHICAL,
        verbose_name="Тег"
    )

    def __str__(self):
        return self.name or f"Изображение {self.id}"

    class Meta:
        verbose_name = "Image upload"
        verbose_name_plural = "Image upload"
        ordering = ['-uploaded_at']