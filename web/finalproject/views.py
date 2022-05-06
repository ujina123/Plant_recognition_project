# JngMkk
from django.shortcuts import render, redirect
from django.http import JsonResponse
from finalproject.models import *
from django.contrib import messages
import datetime

def main(request):
    """ 메인 페이지 """
    # 로그인 상태라면
    if request.user.is_authenticated:
        user = request.user
        userid = AuthUser.objects.filter(username=user).values("id")[0]["id"]
        obj = Plantmanage.objects.filter(username=userid).order_by("nextdate")
        return render(request, "main.html", {"obj": obj})
    else:
        return render(request, "main.html")

def weather(request):
    """ 날씨 정보 REST """
    loc = request.GET.get("loc")
    weather = Weather.objects.filter(si=loc).values("si", "time", "condi", "temp", "humidity", "rainratio", "uv")

    return JsonResponse(list(weather), safe=False, json_dumps_params={"ensure_ascii": False})

def plantinfo(request):
    """ 회원 식물 정보 """
    if request.method == "GET":
        # 현재 세션 유저
        user = request.user
        # userid 불러오기
        userid = AuthUser.objects.filter(username=user).values("id")[0]["id"]
        # D-day 짧은 순으로
        obj = Plantmanage.objects.filter(username=userid).order_by("nextdate")

        return render(request, 'plantinfo.html', {"obj": obj})

    elif request.method == "POST":
        pid = request.POST["waterplant"]
        obj = Plantmanage.objects.get(id=pid)
        now = datetime.date.today()
        # 다음 주기 날짜
        next_date = now + datetime.timedelta(days=obj.cycle)
        # db 업데이트
        Plantmanage.objects.filter(id=pid).update(waterdate=now, nextdate=next_date)
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantdelete(request):
    """ 회원 식물 삭제 """
    if request.method == "GET":
        return redirect("/plantinfo")

    elif request.method == "POST":
        pid = request.POST["deleteplant"]
        # db에서 삭제
        Plantmanage.objects.get(id=pid).delete()
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantmanage(request):
    """ 식물 직접 등록 """ 
    if request.method == "GET":
        return render(request, "plantmanage.html")
    elif request.method == "POST":
        plant_name = request.POST["plant_name"]
        plant_nickname = request.POST["plant_nickname"]
        meet_date = request.POST["plant_date"]
        water_date = request.POST["water_date"]
        water_date = datetime.datetime.strptime(water_date, "%Y-%m-%d").date()
        try:
            plant_id = Plants.objects.get(name=plant_name)
        except:
            messages.add_message(request, messages.ERROR, "아직 저희가 모르는 식물이에요 ㅠㅠ")
            return redirect("/plantmanage")
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

        user = request.user
        user = AuthUser.objects.get(username=user)
        # 새로운 식물 등록 db 저장
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
