from django.urls import reverse
from django.test import TestCase, override_settings
from rest_framework.test import APITestCase
from .models import Prediction, Comment, ImageUpload, PredictionTag
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import IntegrityError

class PredictionModelTest(TestCase):
    def test_prediction_creation(self):
        """Тестирование создания предсказания со всеми полями"""
        prediction = Prediction.objects.create(
            text="Test prediction",
            tag=PredictionTag.PHILOSOPHICAL,
            likes=5
        )
        self.assertEqual(prediction.text, "Test prediction")
        self.assertEqual(prediction.tag, PredictionTag.PHILOSOPHICAL)
        self.assertEqual(prediction.likes, 5)
        self.assertIsNotNone(prediction.created_at)
        
    def test_all_tags_work(self):
        """Проверка всех возможных тегов"""
        for tag in PredictionTag:
            with self.subTest(tag=tag):
                prediction = Prediction.objects.create(tag=tag)
                self.assertEqual(prediction.tag, tag)
    
    def test_image_upload(self):
        """Тестирование загрузки изображения"""
        test_image = SimpleUploadedFile("test.jpg", b"file_content", "image/jpeg")
        prediction = Prediction.objects.create(image=test_image)
        self.assertTrue(prediction.image.name.startswith('predictions/'))
        
    def test_ordering(self):
        """Проверка сортировки по умолчанию"""
        p1 = Prediction.objects.create(text="First")
        p2 = Prediction.objects.create(text="Second")
        self.assertEqual(
            list(Prediction.objects.order_by('-created_at')), 
            [p2, p1]
        )

class CommentModelTest(TestCase):
    def setUp(self):
        self.prediction = Prediction.objects.create(text="Test")
        
    def test_comment_creation(self):
        """Тестирование создания комментария"""
        comment = Comment.objects.create(
            prediction=self.prediction,
            username="user",
            text="Test comment"
        )
        self.assertEqual(comment.prediction, self.prediction)
        self.assertEqual(comment.username, "user")
        self.assertEqual(comment.text, "Test comment")
        self.assertIsNotNone(comment.created_at)
        
    def test_comment_ordering(self):
        """Проверка сортировки комментариев"""
        c1 = Comment.objects.create(prediction=self.prediction, username="1", text="1")
        c2 = Comment.objects.create(prediction=self.prediction, username="2", text="2")
        self.assertEqual(
            list(Comment.objects.order_by('-created_at')), 
            [c2, c1]
        )
        
    def test_comment_required_fields(self):
        """Проверка обязательных полей"""
        with self.assertRaises(IntegrityError):
            Comment.objects.create(prediction=None)

class ImageUploadModelTest(TestCase):
    def test_image_creation(self):
        """Тестирование загрузки изображения"""
        test_file = SimpleUploadedFile("test.jpg", b"content", "image/jpeg")
        img = ImageUpload.objects.create(
            name="Test",
            image=test_file,
            tag=PredictionTag.FUNNY
        )
        self.assertEqual(img.name, "Test")
        self.assertEqual(img.tag, PredictionTag.FUNNY)
        self.assertTrue(img.image.name.startswith('uploads/'))

@override_settings(APPEND_SLASH=False)
class PredictionAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.prediction = Prediction.objects.create(text="API Test")
        cls.comment = Comment.objects.create(
            prediction=cls.prediction,
            username="api_user",
            text="API comment"
        )
        cls.image = ImageUpload.objects.create(name="API Image")
        