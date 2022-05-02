from django.shortcuts import render
from django.http import JsonResponse
from .models import Weather

def index(request):
    return render(request, "main.html")

def weather(request):
    loc = request.GET.get("loc")
    weather = Weather.objects.filter(si=loc).values("si", "time", "condi", "temp", "humidity", "rainratio", "uv")

    return JsonResponse(list(weather), safe=False, json_dumps_params={"ensure_ascii": False})
