# JngMkk
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from finalproject.models import *
from finalproject.forms import PlantForm, PlantRequestForm
from django.contrib import messages
import datetime

def main(request):
    """ 메인 페이지 """
    # 로그인 상태라면
    if request.user.is_authenticated:
        # 유저 id 가져오기
        userid = AuthUser.objects.filter(username=request.user).values("id")[0]["id"]
        # 물을 줘야할 시기가 많이 남지 않은 순으로 정렬
        obj = Plantmanage.objects.filter(userid=userid).order_by("nextdate")
        return render(request, "main.html", {"obj": obj})

    # 비로그인 상태라면
    else:
        return render(request, "main.html")

def weather(request):
    """ 날씨 정보 REST """
    # 위치 정보 받아서
    loc = request.GET.get("loc")
    # 위치에 맞게 날씨 보여줌
    weather = Weather.objects.filter(si=loc).values("si", "time", "condi", "temp", "humidity", "humidinfo", "rainratio", "uv", "uvinfo")
    # Json으로 반환
    return JsonResponse(list(weather), safe=False, json_dumps_params={"ensure_ascii": False})

def plantinfo(request):
    """ 회원 식물 정보 물주기 날짜 업데이트 """
    # POST 요청일 때
    if request.method == "POST":
        # 요청에서 plantid 받아서
        mid = request.POST["manageid"]
        # Plantmanage 테이블에서 plantid에 맞는 레코드 찾고
        obj = Plantmanage.objects.get(manageid=mid)
        # 다음 주기 날짜 = 오늘 날짜 + plantid에 맞는 물줘야하는 주기
        next_date = datetime.date.today() + datetime.timedelta(days=obj.cycle)
        # 물준 날짜, 다음 물주는 날짜 업데이트
        Plantmanage.objects.filter(manageid=mid).update(nextdate=next_date)
        return redirect("/plantinfo")

    # 로그인 상태라면
    if request.user.is_authenticated:
        # userid 불러오기
        userid = AuthUser.objects.filter(username=request.user).values("id")[0]["id"]
        # D-day 짧은 순으로 정렬
        obj = Plantmanage.objects.filter(userid=userid).order_by("nextdate")
        return render(request, 'plantinfo.html', {"obj": obj})

    return render(request, "account/login.html")

def plantdelete(request):
    """ 회원 식물 삭제 """
    if request.method == "POST":
        mid = request.POST.get("deleteplant")
        # db에서 삭제
        Plantmanage.objects.get(manageid=mid).delete()
        return redirect("/plantinfo")

    return redirect("/plantinfo")

def plantmanage(request):
    """ 식물 직접 등록 """
    # POST 요청일 때
    if request.method == "POST":
        form = PlantForm(request.POST)
        # form 검사
        if form.is_valid():
            cycle_dic = {"주 1~2회": 5, "주 1회": 7, "2주 1회": 14, "주 2회": 3, "3주 1회": 21, "월 1회": 30, "2주 1~2회": 10}
            plant_name = request.POST["plant_name"]
            plant_nickname = request.POST["plant_nickname"]
            meet_date = request.POST["plant_date"]
            water_date = request.POST["water_date"]
            water_date = datetime.datetime.strptime(water_date, "%Y-%m-%d").date()
            plant_id = Plants.objects.get(name=plant_name)
            cycle = plant_id.watercycle
            day = cycle_dic[cycle]
            next_date = water_date + datetime.timedelta(days=day)
            user = AuthUser.objects.get(username=request.user)
            # 새로운 식물 등록 db 저장
            pmanage = Plantmanage(userid=user, plantid=plant_id, nickname=plant_nickname, meetdate=meet_date, cycle=day, nextdate=next_date)
            pmanage.save()
            return redirect("/plantinfo")
        
        # form 유효성 검사 실패 시
        else:
            messages.error(request, form.non_field_errors())
            return redirect("/plantmanage")
    
    # POST 요청이 아닐 때
    else:
        # 식물 정보에서 식물 등록으로 넘어왔다면
        if request.GET.get("plant"):
            pid = request.GET.get("plant")
            plant = Plants.objects.filter(plantid=pid).values("name")
            return render(request, "plantmanage.html", {"form": PlantForm(), "plant": plant, 'form2':PlantRequestForm()})
        
        # 로그인 상태라면
        if request.user.is_authenticated:
            return render(request, "plantmanage.html", {"form": PlantForm(), 'form2':PlantRequestForm()})

        # 로그인 상태가 아니라면
        return render(request, "account/login.html")

# 유지 짱짱
def plantrequest(request):
    """ 식물 직접 요청 """
    # POST 요청일 때
    if request.method == "POST":
        form = PlantRequestForm(request.POST)
        # form 검사
        if form.is_valid():
            user = AuthUser.objects.get(username=request.user)
            # 식물 요청 DB 저장
            req = form.save(commit=False)
            req.userid = user
            req.save()
            return redirect("/plantmanage") # 식물등록 페이지로 변경
        else:
            form = PlantRequestForm()
    else:
        if request.user.is_authenticated:
            return redirect("/plantmanage")
        return render(request, "account/login.html")