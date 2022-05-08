# JngMkk
from django.shortcuts import render, redirect
from finalproject.models import Plants, PlantRequest
from finalproject.forms import PlantRequestForm
from elasticsearch import Elasticsearch

def search(word):
    es = Elasticsearch(hosts="localhost", port=9200)
    docs = es.search(index="dictionary",
                    body= {
                        "_source": ["URL", "name"],
                        "query": {
                            "bool": {
                                "must": [{
                                    "match": {
                                        "name.jaso": {
                                            "query": word,
                                            "analyzer": "search_analyzer",
                                            "fuzziness": 1
                                        }
                                    }
                                }],
                                "should": [{
                                    "match": {
                                        "name.ngram": {
                                            "query": word,
                                            "analyzer": "ngram_analyzer"
                                        }
                                    }
                                }]
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

def searching(request):
    if request.GET.get("term"):
        search_word = request.GET.get("term")
        result = search(search_word)
        return render(request, "search_app/search.html", {"result": result})
    return render(request, "search_app/search.html")

def info(request):
    if request.GET.get("id"):
        _id = request.GET.get("id")
        q = Plants.objects.get(plantid=int(_id))
        return render(request, 'search_app/info.html', {"data": q})
    return redirect("search")