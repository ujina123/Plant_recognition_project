# JngMkk
from django.shortcuts import render
from .models import Plants
from elasticsearch import Elasticsearch

def search(request):
    if request.GET.get("term"):
        es = Elasticsearch(hosts="localhost", port=9200)
        search_word = request.GET.get("term")
        docs = es.search(index="dictionary",
                body= {
                    "_source": ["URL", "name"],
                    "query": {
                        "bool": {
                        "must": [
                            {
                            "match": {
                                "name.jaso": {
                                "query": search_word,
                                "analyzer": "search_analyzer"
                                }
                            }
                            }
                        ],
                        "should": [
                            {
                            "match": {
                                "name.ngram": {
                                "query": search_word,
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
        return render(request, "search_app/search.html", {"result" : result})
    else:
        return render(request, 'search_app/search.html')

def info(request):
    if request.method == "GET":
        _id = request.GET.get("id")
        q = Plants.objects.get(plantid=int(_id))
        return render(request, 'search_app/info.html', {"data": q})
    elif request.method == "POST":
        id = request.POST["plant"]
        q = Plants.objects.filter(plantid=id).values("name")
        return render(request, "plantmanage.html", {"data": q})
