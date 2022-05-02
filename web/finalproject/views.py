from django.shortcuts import render, redirect
from django.utils import timezone, dateformat
from finalproject.models import *

def plantinfo(request):
    if request.method == "GET":
        user = request.user
        userid = AuthUser.objects.filter(username=user).values("id")[0]["id"]
        obj = Plantmanage.objects.filter(username=userid)
        return render(request, 'plantinfo.html', {"obj": obj})
    elif request.method == "POST":
        now = dateformat.format(timezone.localtime(), 'Y-m-d')
        pid = request.POST["userplantid"]
        obj = Plantmanage.objects.filter(id=pid).update(waterdate=now)
        return redirect("/plantinfo")
    return redirect("/plantinfo")

def plantmanage(request):
    if request.method == "GET":
        return render(request, "plantmanage.html")
    elif request.method == "POST":
        plant_name = request.POST["plant_name"]
        plant_nickname = request.POST["plant_nickname"]
        meet_date = request.POST["plant_date"]
        water_date = request.POST["water_date"]
        user = request.user

        plant_id = Plants.objects.get(name=plant_name)
        user = AuthUser.objects.get(username=user)
        pmanage = Plantmanage(username=user, plant=plant_id, nickname=plant_nickname, meetdate=meet_date, waterdate=water_date)
        pmanage.save()
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantrecog(request):
    return render(request, 'plantrecog.html')

def plantdisease(request):
    return render(request, 'plantdisease.html')

def plantrecog(request):
    return render(request, 'plantrecog.html')