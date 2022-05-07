from django.shortcuts import render, redirect
from diseaseimage.models import Plantdisease

def getImage(request):
    return render(request, "diseaseimage/plantdisease.html")

def info(request):
    if request.GET.get("id"):
        diseaseid = request.GET.get("id")
        q = Plantdisease.objects.get(diseaseid=diseaseid)
        return render(request, "diseaseimage/diseaseinfo.html", {"data": q})
    return redirect("diseaseimage")