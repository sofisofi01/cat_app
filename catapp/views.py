import random

from django.core.files.storage import default_storage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Prediction, Comment, ImageUpload


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
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "No predictions found"}, status=404)


def home(request):
    return HttpResponse("Добро пожаловать в админку!")


@csrf_exempt
def add_prediction(request):
    if request.method == "POST":
        text = request.POST.get("text")
        image = request.FILES.get("image")
        tag = request.POST.get("tag")
        avatar = request.FILES.get("avatar")

        prediction = Prediction.objects.create(
            text=text,
            image=image,
            tag=tag,
            avatar=avatar,
        )
        return JsonResponse(
            {"id": prediction.id, "message": "Prediction added successfully"}
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def like_prediction(request, prediction_id):
    if request.method == "POST":
        prediction = get_object_or_404(Prediction, id=prediction_id)
        prediction.likes += 1
        prediction.save()
        return JsonResponse({"likes": prediction.likes})
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def add_comment(request, prediction_id):
    if request.method == "POST":
        prediction = get_object_or_404(Prediction, id=prediction_id)
        username = request.POST.get("username")
        text = request.POST.get("text")

        comment = Comment.objects.create(
            prediction=prediction,
            username=username,
            text=text,
        )
        return JsonResponse({"id": comment.id, "message": "Comment added successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        name = request.POST.get("name")
        tag = request.POST.get("tag")

        uploaded_image = ImageUpload.objects.create(
            image=image,
            name=name,
            tag=tag,
        )
        return JsonResponse(
            {"id": uploaded_image.id, "message": "Image uploaded successfully"}
        )
    return JsonResponse({"error": "Invalid request method"}, status=400)
