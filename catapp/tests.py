from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Prediction, Comment, ImageUpload, PredictionTag
from django.core.files.uploadedfile import SimpleUploadedFile

# Юнит-тесты для моделей
class PredictionModelTest(TestCase):
    def test_create_prediction_with_text(self):
        prediction = Prediction.objects.create(
            text="Test prediction",
            tag=PredictionTag.PHILOSOPHICAL,
        )
        self.assertEqual(prediction.text, "Test prediction")
        self.assertEqual(prediction.tag, PredictionTag.PHILOSOPHICAL)
        self.assertEqual(prediction.likes, 0)

    def test_create_prediction_with_image(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        prediction = Prediction.objects.create(
            text="Test prediction with image",
            image=image,
            tag=PredictionTag.FUNNY,
        )
        self.assertEqual(prediction.text, "Test prediction with image")
        self.assertEqual(prediction.tag, PredictionTag.FUNNY)
        self.assertIsNotNone(prediction.image)

    def test_create_prediction_with_avatar(self):
        avatar = SimpleUploadedFile("test_avatar.jpg", b"file_content", content_type="image/jpeg")
        prediction = Prediction.objects.create(
            text="Test prediction with avatar",
            avatar=avatar,
            tag=PredictionTag.INSPIRATIONAL,
        )
        self.assertEqual(prediction.text, "Test prediction with avatar")
        self.assertEqual(prediction.tag, PredictionTag.INSPIRATIONAL)
        self.assertIsNotNone(prediction.avatar)

    def test_prediction_str_method(self):
        prediction = Prediction.objects.create(
            text="Test prediction",
            tag=PredictionTag.PHILOSOPHICAL,
        )
        self.assertEqual(str(prediction), "Test prediction")


class CommentModelTest(TestCase):
    def test_create_comment(self):
        prediction = Prediction.objects.create(text="Test prediction")
        comment = Comment.objects.create(
            prediction=prediction,
            username="test_user",
            text="Test comment",
        )
        self.assertEqual(comment.username, "test_user")
        self.assertEqual(comment.text, "Test comment")
        self.assertEqual(comment.prediction, prediction)

    def test_comment_str_method(self):
        prediction = Prediction.objects.create(text="Test prediction")
        comment = Comment.objects.create(
            prediction=prediction,
            username="test_user",
            text="Test comment",
        )
        self.assertEqual(str(comment), f"Comment by {comment.username}")


class ImageUploadModelTest(TestCase):
    def test_create_image_upload(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        image_upload = ImageUpload.objects.create(
            name="Test image",
            image=image,
            tag=PredictionTag.FUNNY,
        )
        self.assertEqual(image_upload.name, "Test image")
        self.assertEqual(image_upload.tag, PredictionTag.FUNNY)
        self.assertIsNotNone(image_upload.image)

    def test_image_upload_str_method(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        image_upload = ImageUpload.objects.create(
            name="Test image",
            image=image,
            tag=PredictionTag.FUNNY,
        )
        self.assertEqual(str(image_upload), f"Image {image_upload.id}")


# Интеграционные тесты для API
class PredictionAPITest(APITestCase):
    def setUp(self):
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
        url = reverse("random_prediction")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("text", response.json())

    # def test_add_comment(self):
    #     url = reverse("add_comment", args=[self.prediction.id])
    #     data = {
    #         "username": "new_user",
    #         "text": "New comment",
    #     }
    #     response = self.client.post(url, data, format="json")
    #     print(response.content)  # Для отладки
    #     self.assertEqual(response.status_code, 201)  # Ожидаем статус 201 Created
    #     self.assertEqual(response.json()["username"], "new_user")
    #     self.assertEqual(response.json()["text"], "New comment")

    # def test_upload_image(self):
    #     url = reverse("upload_image")
    #     image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    #     data = {
    #         "name": "Test image",
    #         "tag": PredictionTag.FUNNY,
    #         "image": image,
    #     }
    #     response = self.client.post(url, data, format="multipart")
    #     print(response.content)  # Для отладки
    #     self.assertEqual(response.status_code, 201)  # Ожидаем статус 201 Created
    #     self.assertEqual(response.json()["name"], "Test image")
    #     self.assertEqual(response.json()["tag"], PredictionTag.FUNNY)

    def test_get_all_images(self):
        url = reverse("get_all_images")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("images", response.json())

    def test_get_image_details(self):
        url = reverse("get_image_details", args=[self.image_upload.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("name", response.json())

    def test_get_all_predictions(self):
        url = reverse("get_all_predictions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("predictions", response.json())

    def test_get_comments_for_prediction(self):
        url = reverse("get_comments_for_prediction", args=[self.prediction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("comments", response.json())

    def test_get_nonexistent_prediction(self):
        url = reverse("get_image_details", args=[999])  # Несуществующий ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_add_comment_invalid_data(self):
        url = reverse("add_comment", args=[self.prediction.id])
        data = {
            "username": "",  # Пустое имя пользователя
            "text": "New comment",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 400)  # Ожидаем статус 400 Bad Request