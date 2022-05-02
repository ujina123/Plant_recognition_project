# JngMkk
from django.shortcuts import render
from django.http import JsonResponse
from weather_app.models import Weather, AuthUser
from finalproject.models import Plantmanage

def index(request):
    user = request.user
    userid = AuthUser.objects.filter(username=user).values("id")[0]["id"]
    obj = Plantmanage.objects.filter(id=userid).order_by("nextdate")
    return render(request, "main.html", {"obj": obj})

def weather(request):
    loc = request.GET.get("loc")
    weather = Weather.objects.filter(si=loc).values("si", "time", "condi", "temp", "humidity", "rainratio", "uv")

    return JsonResponse(list(weather), safe=False, json_dumps_params={"ensure_ascii": False})
