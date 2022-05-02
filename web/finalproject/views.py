# JngMkk
from django.shortcuts import render, redirect
from django.utils import timezone, dateformat
from finalproject.models import *
import datetime

def plantinfo(request):
    if request.method == "GET":
        user = request.user
        userid = AuthUser.objects.filter(username=user).values("id")[0]["id"]
        obj = Plantmanage.objects.filter(username=userid)
        return render(request, 'plantinfo.html', {"obj": obj})

    elif request.method == "POST":
        pid = request.POST["waterplant"]
        obj = Plantmanage.objects.get(id=pid)
        now = datetime.datetime.strptime(dateformat.format(timezone.localtime(), 'Y-m-d'), "%Y-%m-%d")
        next_date = now + datetime.timedelta(days=obj.cycle)
        Plantmanage.objects.filter(id=pid).update(waterdate=now, nextdate=next_date)
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantdelete(request):
    if request.method == "GET":
        return redirect("/plantinfo")

    elif request.method == "POST":
        pid = request.POST["deleteplant"]
        Plantmanage.objects.get(id=pid).delete()
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
        water_date = datetime.datetime.strptime(water_date, "%Y-%m-%d")

        user = request.user

        plant_id = Plants.objects.get(name=plant_name)
        cycle = plant_id.watercycle

        if cycle == "주 1~2회":
            day=5
            next_date = water_date + datetime.timedelta(days=day)
        elif cycle == "주 1회":
            day=7
            next_date = water_date + datetime.timedelta(days=day)
        elif cycle == "2주 1회":
            day=14
            next_date = water_date + datetime.timedelta(days=day)
        elif cycle == "주 2회":
            day=3
            next_date = water_date + datetime.timedelta(days=day)
        elif cycle == "3주 1회":
            day=21
            next_date = water_date + datetime.timedelta(days=day)
        elif cycle == "월 1회":
            day=30
            next_date = water_date + datetime.timedelta(days=day)
        else:
            day=10
            next_date = water_date + datetime.timedelta(days=day)

        user = AuthUser.objects.get(username=user)
        pmanage = Plantmanage(username=user, plant=plant_id, nickname=plant_nickname, meetdate=meet_date, waterdate=water_date, cycle=day, nextdate=next_date)
        pmanage.save()
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantrecog(request):
    return render(request, 'plantrecog.html')

def plantdisease(request):
    return render(request, 'plantdisease.html')

def plantrecog(request):
    return render(request, 'plantrecog.html')