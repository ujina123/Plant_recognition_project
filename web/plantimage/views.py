import io
import re
from PIL import Image as im
import torch
from django.shortcuts import render, redirect
from finalproject.models import AuthUser, Plants
from plantimage.models import PlantModel
from diseaseimage.forms import ImageUpload
from django.contrib import messages


plant_dic ={'orangejasmin':'오렌지 자스민', 'benghaltree':'벵갈 고무나무', 'stuckyi':'스투키', 'rosmari':'로즈마리', 'ivy':'아이비', 'geumjeonsoo':'금전수',
            'yeoincho':'여인초', 'wilma':'율마', 'skindapsus':'스킨답서스', 'sansevieria':'산세베리아', 'hongkong':'홍콩 야자', 'sanhosoo':'산호수', 
            'gaewoonjuk':'개운죽', 'tableyaja':'테이블 야자', 'hangwoonmok':'행운목', 'monstera':'몬스테라'}

def getImage(request):
    """ 식물 인식 모델 """
    # 요청 들어오면
    if request.method == "POST":
        form = ImageUpload(request.POST, request.FILES)
        
        # 요청에서 img 가져오고
        if form.is_valid():
            imgfile = request.FILES["image"]
            print(imgfile.size, imgfile.name, imgfile.file,
                imgfile.content_type, imgfile.field_name)

            # 로그인 중이라면
            if request.user.is_authenticated:
                userid = AuthUser.objects.get(username=request.user)
            # 아니라면
            else:
                userid = None
            # PlantModel에 저장
            img_instance = PlantModel(userid=userid, image=imgfile)
            img_instance.save()
            
            # PlantModel에 마지막에 저장된 img
            uploaded_img_qs = PlantModel.objects.filter().last()
            uploaded_img_str = str(uploaded_img_qs.image).split("/")[1].rsplit(".")[0]
            # img읽기
            img_bytes = uploaded_img_qs.image.read()
            # img열기
            img = im.open(io.BytesIO(img_bytes))
            
            # yolov5 디렉터리
            path_hubconfig = "yolo_plant"
            # 인식모델 파일
            path_weightfile = "yolo_plant/runs/train/yolov5s_results20/weights/best.pt"  

            # 모델 불러오기
            model = torch.hub.load(path_hubconfig, 'custom', path=path_weightfile, source='local')
            
            # 예측 confidence 기준 50%로 설정
            model.conf = 0.5
            
            # 모델 결과 
            results = model(img, size=224)
            
            try: 
            # 인식값 나오면
                res_table = results.pandas().xyxy[0] # 결과 테이블 저장 
                result_list = [res_table['confidence'].values] # 결과 테이블에서 confidence를 result_list에 저장
                res_idx = result_list.index(max(result_list)) # confidence를 저장한 result_list에서 가장 큰 값 인덱스 찾기 
                
                result_confidence = res_table['confidence'].values[res_idx] # confidenc가 가장 높은 것
                result_name = plant_dic[res_table['name'].values[res_idx]] # confidenc가 가장 높이 예측된 식물
                plant = Plants.objects.filter(name__contains=result_name)
                plant_name = plant[0].plantid

            except:
                # 안나오면
                result_confidence = None
                plant_name = None
            
            # 모델 돌린거 render
            results.render()
            
            # media/plant_out에 결과 저장
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save(f"media/plant_out/{uploaded_img_str}_out.jpg", format="JPEG")

            # 결과 내용 PlantModel에 업데이트
            PlantModel.objects.filter(plmodelid=uploaded_img_qs.plmodelid).update(plantid=plant_name, accuracy=result_confidence, outimage=f"plant_out/{uploaded_img_str}_out.jpg")
            
            # 이름 None일 경우 메시지
            ## yujin ##
            if plant_name is None:
                messages.warning(request, "식물을 인식하지 못했어요")
                messages.warning(request, "식물이 잘 보이게 찍어주세요!")
                return redirect("/plantrecog")

            return render(request, "plantimage/plantrecog.html", {"form": ImageUpload(), "plants": plant})
        return redirect("/plantrecog")
    return render(request, "plantimage/plantrecog.html", {"form": ImageUpload()})