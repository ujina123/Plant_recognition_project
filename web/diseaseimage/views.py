# JngMkk
from django.shortcuts import render, redirect
from diseaseimage.models import Plantdisease, DiseaseModel
from finalproject.models import AuthUser
from diseaseimage.forms import ImageUpload
from django.contrib import messages
import io
from PIL import Image as im
import torch

def getImage(request):
    """ 식물 인식 모델 """
    # 요청 들어오면
    if request.method == "POST":
        # 요청에서 img 가져오고
        form = ImageUpload(request.POST, request.FILES)
        if form.is_valid():
            imgfile = request.FILES.get("image")
            # 로그인 중이라면
            if request.user.is_authenticated:
                userid = AuthUser.objects.get(username=request.user)
            # 아니라면
            else:
                userid = None

            img_instance = DiseaseModel(username=userid, image=imgfile)
            img_instance.save()

            uploaded_img_qs = DiseaseModel.objects.filter().last()
            uploaded_img_str = str(uploaded_img_qs.image).split("/")[1].rsplit(".")[0]
            # img읽기
            img_bytes = uploaded_img_qs.image.read()
            # img열기
            img = im.open(io.BytesIO(img_bytes))

            # yolov5 디렉터리
            path_hubconfig = "yolo_disease"
            # 인식모델 파일
            path_weightfile = "yolo_disease/runs/train/yolov5s_results_ver5/weights/best.pt"  

            model = torch.hub.load(path_hubconfig, 'custom', path=path_weightfile, source='local')
            results = model(img, size=224)
            
            try:
                # 인식값 나오면
                result_confidence = results.pandas().xyxy[0]['confidence'].values[0]
                result_name = results.pandas().xyxy[0]['name'].values[0]
            except:
                # 안나오면
                result_confidence = None
                result_name = None

            print('--'*10)
            print('pred_name: ',result_name, '\nconfidence: ' , result_confidence)
            
            # 모델 돌린거 render
            results.render()

            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save(f"media/disease_out/{uploaded_img_str}_out.jpg", format="JPEG")

            # 결과 이름, 정확도, 이미지 경로 db저장
            DiseaseModel.objects.filter(id=uploaded_img_qs.id).update(name=result_name, accuracy=result_confidence, outimage=f"disease_out/{uploaded_img_str}_out.jpg")

            # 이름 None일 경우 메세지
            if result_name is None:
                messages.warning(request, "식물병을 인식하지 못했어요")
                messages.warning(request, "식물병이 잘 보이게 찍어주세요")
                return redirect("/plantdisease")
            
            # 이름 None 아닐 경우 이름 return
            return render(request, "diseaseimage/plantdisease.html", {"form": ImageUpload(), "disease": result_name})
        return redirect("/plantdisease")
    return render(request, "diseaseimage/plantdisease.html", {"form": ImageUpload()})

def info(request):
    if request.GET.get("id"):
        diseaseid = request.GET.get("id")
        q = Plantdisease.objects.get(diseaseid=diseaseid)
        return render(request, "diseaseimage/diseaseinfo.html", {"data": q})
    return redirect("diseaseimage")