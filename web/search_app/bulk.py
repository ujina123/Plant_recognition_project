import json
from elasticsearch import Elasticsearch

es = Elasticsearch([{'host':'localhost','port':'9200'}])

es.indices.create(
    index="dictionary",
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        },
                        "english" : {
                            "type": "custom",
                            "tokenizer": "standard",
                            "filter" : [
                                "lowercase"
                            ]
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
                    "analyzer": "my_analyzer"
                },
                "botanyNm": {
                    "type": "text",
                    "analyzer": "english"
                }
            }
        }
    }
)

file = "/Users/younwoo/Downloads/plantName.json"
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