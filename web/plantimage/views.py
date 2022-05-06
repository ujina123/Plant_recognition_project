import io
from PIL import Image as im
import torch
from django.shortcuts import render
from finalproject.models import AuthUser
from plantimage.models import ImageModel
from elasticsearch import Elasticsearch
from django.contrib import messages
# from .forms import ImageUploadForm

def search(word):
    es = Elasticsearch(hosts="localhost", port=9200)
    docs = es.search(index="dictionary",
            body= {
                "_source": ["URL", "name"],
                "query": {
                    "bool": {
                    "must": [
                        {
                        "match": {
                            "name.jaso": {
                            "query": word,
                            "analyzer": "search_analyzer"
                            }
                        }
                        }
                    ],
                    "should": [
                        {
                        "match": {
                            "name.ngram": {
                            "query": word,
                            "analyzer": "ngram_analyzer"
                            }
                        }
                        }
                    ]
                    }
                },
                "highlight": {
                    "fields": {
                    "name.ngram": {}
                    }
                }
            })
    data = docs["hits"]["hits"]
    result = []
    for d in data:
        result.append([d["_id"], d["_source"]["URL"], d["_source"]["name"]])
    return result

def getImage(request):
    if request.method == "GET":
        return render(request, "plantimage/plantrecog.html")
    elif request.method == "POST":
        img = request.FILES["plant_img"]
        user = request.user
        try:
            userid = AuthUser.objects.get(username=user)
        except:
            userid = None
        img_instance = ImageModel(username=userid, image=img)
        img_instance.save()
        
        uploaded_img_qs = ImageModel.objects.filter().last()
        img_bytes = uploaded_img_qs.image.read()
        img = im.open(io.BytesIO(img_bytes))

        path_hubconfig = "yolov5_code"
        path_weightfile = "yolov5_code/runs/train/yolov5s_results20/weights/best.pt"  

        model = torch.hub.load(path_hubconfig, 'custom', path=path_weightfile, source='local')
        results = model(img, size=224)
        
        try:
            result_confidence = results.pandas().xyxy[0]['confidence'].values[0]
            result_name = results.pandas().xyxy[0]['name'].values[0]
        except:
            result_confidence = None
            result_name = ""

        print('--'*10)
        print('pred_name: ',result_name, '\nconfidence: ' , result_confidence)
        
        results.render()
        
        for img in results.imgs:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out/image0.jpg", format="JPEG")

        # form = ImageUploadForm()
        ImageModel.objects.filter(id=uploaded_img_qs.id).update(name=result_name, accuracy=result_confidence)
        if result_name == "monstera":
            result_name = "몬스테라"
        plants = search(result_name)
        # context = {
        #     "form": form,
        #     "plants": plants
        # }
        return render(request, "plantimage/plantrecog.html", {"plants": plants})
    return render(request, "plantimage/plantrecog.html")