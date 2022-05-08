import io
from PIL import Image as im
import torch
from django.shortcuts import render, redirect
from finalproject.models import AuthUser
from plantimage.models import PlantModel
from search_app.views import search
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
            imgfile = request.FILES.get("image")
            # 로그인 중이라면
            if request.user.is_authenticated:
                userid = AuthUser.objects.get(username=request.user)
            # 아니라면
            else:
                userid = None
            # PlantModel에 저장
            img_instance = PlantModel(username=userid, image=imgfile)
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

            model = torch.hub.load(path_hubconfig, 'custom', path=path_weightfile, source='local')
            results = model(img, size=224)
            
            try:
                # 인식값 나오면
                result_confidence = results.pandas().xyxy[0]['confidence'].values[0]
                result_name = plant_dic[results.pandas().xyxy[0]['name'].values[0]]
            except:
                # 안나오면
                result_confidence = None
                result_name = None

            print('--'*10)
            print('pred_name: ',result_name, '\nconfidence: ' , result_confidence)
            
            # 모델 돌린거 render
            results.render()
            
            # media/plant_out에 결과 저장
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save(f"media/plant_out/{uploaded_img_str}_out.jpg", format="JPEG")

            # 결과 내용 PlantModel에 업데이트
            PlantModel.objects.filter(id=uploaded_img_qs.id).update(name=result_name, accuracy=result_confidence, outimage=f"plant_out/{uploaded_img_str}_out.jpg")
            
            # 이름 None일 경우 메시지
            if result_name is None:
                messages.warning(request, "식물 인식에 실패했어요ㅠㅠ")
                return redirect("/plantrecog")
            
            # 이름 None 아닐 경우 elasticsearch 검색
            plants = search(result_name)

            return render(request, "plantimage/plantrecog.html", {"form": ImageUpload(), "plants": plants})
        return redirect("/plantrecog")
    return render(request, "plantimage/plantrecog.html", {"form": ImageUpload()})