from django.shortcuts import render

def getImage(request):
    return render(request, "diseaseimage/plantdisease.html")