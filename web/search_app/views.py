# JngMkk
from django.shortcuts import render, redirect
from search_app.models import Plants
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
    if request.GET.get("id"):
        _id = request.GET.get("id")
        q = Plants.objects.get(plantid=int(_id))
        return render(request, 'search_app/info.html', {"data": q})
    return redirect("search")