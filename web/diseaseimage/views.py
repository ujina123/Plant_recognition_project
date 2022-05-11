from django.shortcuts import render, redirect
from diseaseimage.models import Plantdisease, DiseaseModel
from finalproject.models import AuthUser
from diseaseimage.forms import ImageUpload
from django.utils.safestring import mark_safe
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

            img_instance = DiseaseModel(userid=userid, image=imgfile)
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
            model.conf = 0.2
            results = model(img, size=224)
            
            try:
                # 인식값 나오면
                res_table = results.pandas().xyxy[0] # 결과 테이블 저장 
                result_name_list = res_table['name'].values.tolist()
                result_conf_list = res_table['confidence'].values.tolist()
                
                # yujin #
                list_conf = []
                if '정상' in result_name_list:
                    if '흰가루병' in result_name_list:
                        powdery_conf = [result_conf_list[i] for i, value in enumerate(result_name_list) if value == '흰가루병']
                        list_conf.append(powdery_conf[0])
                    if '노균병' in result_name_list:
                        downy_conf = [result_conf_list[i] for i, value in enumerate(result_name_list) if value == '노균병']
                        list_conf.append(downy_conf[0])
                    if ('노균병' not in result_name_list) & ('흰가루병' not in result_name_list):
                        nor_conf = [result_conf_list[i] for i, value in enumerate(result_name_list) if value == '정상']
                        list_conf.append(nor_conf[0])
                else:
                    if '흰가루병' in result_name_list:
                        powdery_conf = [result_conf_list[i] for i, value in enumerate(result_name_list) if value == '흰가루병']
                        list_conf.append(powdery_conf[0])
                    if '노균병' in result_name_list:
                        downy_conf = [result_conf_list[i] for i, value in enumerate(result_name_list) if value == '노균병']
                        list_conf.append(downy_conf[0])

                max_idx = result_conf_list.index(max(list_conf))
                
                result_confidence = result_conf_list[max_idx]
                result_name = result_name_list[max_idx]
                if result_name != "정상":
                    result_name = Plantdisease.objects.filter(diseasename=result_name).values("diseaseid")[0]["diseaseid"]
                    print(result_name)

            except:
                # 안나오면
                result_confidence = None
                result_name = None
            
            # 모델 돌린거 render
            results.render()

            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save(f"media/disease_out/{uploaded_img_str}_out.jpg", format="JPEG")

            # 결과 이름, 정확도, 이미지 경로 db저장
            DiseaseModel.objects.filter(dsmodelid=uploaded_img_qs.dsmodelid).update(diseaseid=result_name, accuracy=result_confidence, outimage=f"disease_out/{uploaded_img_str}_out.jpg")

            # 이름 None일 경우 메세지
            if result_name is None:
                messages.warning(request, mark_safe("식물병을 인식하지 못했어요.<br/>식물병이 잘 보이게 찍어주세요."))
                return redirect("/plantdisease")
            elif result_name == "정상":
                messages.info(request, mark_safe("발견된 식물병이 없습니다.<br/>식물도 사람처럼 사랑을 주세요!<br/>내 식물과 더 친해지기 👉 "))
                return redirect("/plantdisease")

            return render(request, "diseaseimage/plantdisease.html", {"form": ImageUpload(), "d": Plantdisease.objects.get(diseaseid=result_name), "per": result_confidence})
        return redirect("/plantdisease")
    return render(request, "diseaseimage/plantdisease.html", {"form": ImageUpload()})

def info(request):
    if request.GET.get("id"):
        diseaseid = request.GET.get("id")
        q = Plantdisease.objects.get(diseaseid=diseaseid)
        return render(request, "diseaseimage/diseaseinfo.html", {"data": q})
    return redirect("diseaseimage")