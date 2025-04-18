# Generated by Django 5.1.6 on 2025-03-29 15:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catapp", "0004_alter_imageupload_image"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterModelOptions(
            name="imageupload",
            options={
                "ordering": ["-uploaded_at"],
                "verbose_name": "Загруженное изображение",
                "verbose_name_plural": "Загруженные изображения",
            },
        ),
        migrations.AlterField(
            model_name="comment",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата создания"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="prediction",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="catapp.prediction",
                verbose_name="Предсказание",
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="text",
            field=models.TextField(max_length=300, verbose_name="Текст"),
        ),
        migrations.AlterField(
            model_name="comment",
            name="username",
            field=models.CharField(max_length=100, verbose_name="Имя пользователя"),
        ),
        migrations.AlterField(
            model_name="imageupload",
            name="image",
            field=models.ImageField(
                upload_to="uploads/%Y/%m/%d/", verbose_name="Изображение"
            ),
        ),
        migrations.AlterField(
            model_name="imageupload",
            name="name",
            field=models.CharField(max_length=300, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="imageupload",
            name="tag",
            field=models.CharField(
                choices=[
                    ("philosophical", "Философское"),
                    ("funny", "Смешное"),
                    ("inspirational", "Жизнеутверждающее"),
                    ("domestic", "Домашнее"),
                    ("relax", "Релакс"),
                    ("dreams", "Мечты"),
                    ("trivial", "Мелочи"),
                    ("nostalgia", "Ностальгия"),
                    ("mysterious", "Загадочное"),
                    ("fate", "Судьба"),
                    ("everyday", "Бытовое"),
                ],
                default="philosophical",
                max_length=20,
                verbose_name="Тег",
            ),
        ),
        migrations.AlterField(
            model_name="imageupload",
            name="uploaded_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки"),
        ),
    ]
