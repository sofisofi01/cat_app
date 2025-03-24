import random

from django.core.files.storage import default_storage
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Comment, ImageUpload, Prediction


@swagger_auto_schema(
    method="get",
    responses={
        200: openapi.Response(
            description="Случайное предсказание",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "text": openapi.Schema(type=openapi.TYPE_STRING),
                    "image": openapi.Schema(type=openapi.TYPE_STRING),
                    "likes": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "tag": openapi.Schema(type=openapi.TYPE_STRING),
                    "avatar": openapi.Schema(type=openapi.TYPE_STRING),
                },
            ),
        ),
        404: openapi.Response(description="Предсказания не найдены"),
    },
)
@api_view(["GET"])
def get_random_prediction(request):
    predictions = Prediction.objects.all()
    if predictions:
        random_prediction = random.choice(predictions)
        data = {
            "id": random_prediction.id,
            "text": random_prediction.text,
            "image": random_prediction.image.url if random_prediction.image else None,
            "likes": random_prediction.likes,
            "tag": random_prediction.tag,
            "avatar": (
                random_prediction.avatar.url if random_prediction.avatar else None
            ),
        }
        return JsonResponse(data, json_dumps_params={"ensure_ascii": False})
    else:
        return JsonResponse(
            {"error": "No predictions found"},
            status=404,
            json_dumps_params={"ensure_ascii": False},
        )


def home(request):
    return HttpResponse("Добро пожаловать в админку!")


@api_view(["POST"])
def add_prediction(request):
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("image")
        tag = request.POST.get("tag")
        avatar = request.FILES.get("avatar")

        if not text:
            return JsonResponse(
                {"error": "Text is required"},
                status=400,
                json_dumps_params={"ensure_ascii": False},
            )

        prediction = Prediction.objects.create(
            text=text,
            image=image,
            tag=tag,
            avatar=avatar,
        )
        return JsonResponse(
            {"id": prediction.id, "message": "Prediction added successfully"},
            json_dumps_params={"ensure_ascii": False},
        )
    return JsonResponse(
        {"error": "Invalid request method"},
        status=400,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["POST"])
def like_prediction(request, prediction_id):
    if request.method == "POST":
        prediction = get_object_or_404(Prediction, id=prediction_id)
        prediction.likes += 1
        prediction.save()
        return JsonResponse(
            {"likes": prediction.likes}, json_dumps_params={"ensure_ascii": False}
        )
    return JsonResponse(
        {"error": "Invalid request method"},
        status=400,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["POST"])
def add_comment(request, prediction_id):
    if request.method == "POST":
        prediction = get_object_or_404(Prediction, id=prediction_id)
        username = request.POST.get("username")
        text = request.POST.get("text")

        if not username or not text:
            return JsonResponse(
                {"error": "Username and text are required"},
                status=400,
                json_dumps_params={"ensure_ascii": False},
            )

        comment = Comment.objects.create(
            prediction=prediction,
            username=username,
            text=text,
        )
        return JsonResponse(
            {"id": comment.id, "message": "Comment added successfully"},
            json_dumps_params={"ensure_ascii": False},
        )
    return JsonResponse(
        {"error": "Invalid request method"},
        status=400,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["POST"])
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        tag = request.POST.get("tag")

        if not image or not name:
            return JsonResponse(
                {"error": "Image and name are required"},
                status=400,
                json_dumps_params={"ensure_ascii": False},
            )

        uploaded_image = ImageUpload.objects.create(
            image=image,
            name=name,
            tag=tag,
        )
        return JsonResponse(
            {"id": uploaded_image.id, "message": "Image uploaded successfully"},
            json_dumps_params={"ensure_ascii": False},
        )
    return JsonResponse(
        {"error": "Invalid request method"},
        status=400,
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["GET"])
def get_all_images(request):
    tag_filter = request.GET.get("tag")
    sort_by_date = request.GET.get("sort") == "date"
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    images = ImageUpload.objects.all()

    if tag_filter:
        images = images.filter(tag=tag_filter)

    if sort_by_date:
        images = images.order_by("-uploaded_at")

    paginator = Paginator(images, page_size)
    page = paginator.get_page(page_number)

    images_data = [
        {
            "id": image.id,
            "name": image.name,
            "image": image.image.url if image.image else None,
            "uploaded_at": image.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
            "tag": image.tag,
        }
        for image in page
    ]

    return JsonResponse(
        {
            "images": images_data,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
        },
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["GET"])
def get_image_details(request, image_id):
    image = get_object_or_404(ImageUpload, id=image_id)
    data = {
        "id": image.id,
        "name": image.name,
        "image": image.image.url if image.image else None,
        "uploaded_at": image.uploaded_at.strftime("%Y-%m-%d %H:%M:%S"),
        "tag": image.tag,
    }

    return JsonResponse(data, json_dumps_params={"ensure_ascii": False})


@api_view(["GET"])
def get_all_predictions(request):
    sort_by_likes = request.GET.get("sort") == "likes"
    order = request.GET.get("order", "desc")
    tag_filter = request.GET.get("tag")
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 10)

    predictions = Prediction.objects.all()

    if tag_filter:
        predictions = predictions.filter(tag=tag_filter)

    if sort_by_likes:
        if order == "asc":
            predictions = predictions.order_by("likes")
        else:
            predictions = predictions.order_by("-likes")

    paginator = Paginator(predictions, page_size)
    page = paginator.get_page(page_number)

    predictions_data = [
        {
            "id": prediction.id,
            "text": prediction.text,
            "image": prediction.image.url if prediction.image else None,
            "likes": prediction.likes,
            "tag": prediction.tag,
            "avatar": prediction.avatar.url if prediction.avatar else None,
        }
        for prediction in page  # Используем page вместо predictions
    ]

    return JsonResponse(
        {
            "predictions": predictions_data,
            "total_pages": paginator.num_pages,
            "current_page": page.number,
        },
        json_dumps_params={"ensure_ascii": False},
    )


@api_view(["GET"])
def get_comments_for_prediction(request, prediction_id):
    prediction = get_object_or_404(Prediction, id=prediction_id)

    comments = Comment.objects.filter(prediction=prediction)

    comments_data = [
        {
            "id": comment.id,
            "username": comment.username,
            "text": comment.text,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for comment in comments
    ]

    return JsonResponse(
        {"comments": comments_data}, json_dumps_params={"ensure_ascii": False}
    )
