from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Prediction, Comment, ImageUpload, PredictionTag


# Юнит-тесты для моделей
class PredictionModelTest(TestCase):
    def test_create_prediction(self):
        # Создаем объект Prediction
        prediction = Prediction.objects.create(
            text="Test prediction",
            tag=PredictionTag.PHILOSOPHICAL,
        )
        # Проверяем, что объект создан корректно
        self.assertEqual(prediction.text, "Test prediction")
        self.assertEqual(prediction.tag, PredictionTag.PHILOSOPHICAL)
        self.assertEqual(prediction.likes, 0)  # По умолчанию likes = 0


class CommentModelTest(TestCase):
    def test_create_comment(self):
        # Создаем объект Prediction
        prediction = Prediction.objects.create(text="Test prediction")
        # Создаем объект Comment
        comment = Comment.objects.create(
            prediction=prediction,
            username="test_user",
            text="Test comment",
        )
        # Проверяем, что объект создан корректно
        self.assertEqual(comment.username, "test_user")
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.prediction, prediction)


class ImageUploadModelTest(TestCase):
    def test_create_image_upload(self):
        # Создаем объект ImageUpload
        image_upload = ImageUpload.objects.create(
            name="Test image",
            tag=PredictionTag.FUNNY,
        )
        # Проверяем, что объект создан корректно
        self.assertEqual(image_upload.name, "Test image")
        self.assertEqual(image_upload.tag, PredictionTag.FUNNY)


# Интеграционные тесты для API
class PredictionAPITest(APITestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.prediction = Prediction.objects.create(
            text="Test prediction",
            tag=PredictionTag.PHILOSOPHICAL,
        )
        self.comment = Comment.objects.create(
            prediction=self.prediction,
            username="test_user",
            text="Test comment",
        )
        self.image_upload = ImageUpload.objects.create(
            name="Test image",
            tag=PredictionTag.FUNNY,
        )

    def test_get_random_prediction(self):
        url = reverse("random_prediction") + "/"  # Добавьте "/" в конце
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text", response.json())

    def test_add_comment(self):
        url = reverse("add_comment", args=[self.prediction.id]) + "/"  # Добавьте "/" в конце
        data = {
            "username": "new_user",
            "text": "New comment",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Comment added successfully")

    def test_upload_image(self):
        url = reverse("upload_image") + "/"  # Добавьте "/" в конце
        with open("catapp/tests/test_image.jpg", "rb") as image:
            data = {
                "name": "Test image",
                "tag": PredictionTag.FUNNY,
                "image": image,
            }
            response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Image uploaded successfully")