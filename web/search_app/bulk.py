# JngMkk
# ElasticSearch 7.16.2
# jaso 7.16.2
# kibana 7.16.2
import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.create(
    index="dictionary",
    body={
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "max_ngram_diff": 30,
                "analysis": {
                    "filter": {
                        "ngram_filter": {
                            "type": "edge_ngram",
                            "min_gram": 5,
                            "max_gram": 30
                        }
                    },
                    "analyzer": {
                        "ngram_analyzer": {
                            "type": "custom",
                            "tokenizer": "ngram_tokenizer"
                        },
                        "search_analyzer": {
                            "type": "custom",
                            "tokenizer": "jaso_search_tokenizer",
                        },
                        "index_analyzer": {
                            "type": "custom",
                            "tokenizer": "jaso_index_tokenizer",
                            "filter": [
                                "ngram_filter"
                            ]
                        },
                    },
                    "tokenizer": {
                        "jaso_search_tokenizer": {
                            "type": "jaso_tokenizer",
                            "mistype": True,
                            "chosung": False
                        },
                        "jaso_index_tokenizer": {
                            "type": "jaso_tokenizer",
                            "mistype": True,
                            "chosung": True
                        },
                        "ngram_tokenizer": {
                            "type": "ngram",
                            "min_gram": 2,
                            "max_gram": 10
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "URL": {
                    "type": "keyword",
                },
                "name": {
                    "type": "text",
                    "fields": {
                        "ngram": {
                            "type": "text",
                            "analyzer": "ngram_analyzer"
                        },
                        "jaso": {
                            "type": "text",
                            "analyzer": "index_analyzer"                            
                        }
                    }
                },
            }
        }
    }
)

file = "/home/ubuntu/finalproject/dags/data/plantName.json"
with open(file, encoding="utf-8") as file:
    json_data = json.loads(file.read())

body = ""
count = 1
for i in json_data:
    body = body + json.dumps({"index": {"_index": "dictionary", "_id": count}}) + "\n"
    body = body + json.dumps(i, ensure_ascii=False) + "\n"
    if count == 1:
        print(body)
    count += 1

es.bulk(body)
