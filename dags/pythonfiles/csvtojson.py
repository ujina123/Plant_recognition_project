#-*- coding: utf-8 -*-
import csv
import json

def csv_to_json(inputfile, outputfile):
    data = []
    with open(inputfile, 'rt', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            data.append(r)

    with open(outputfile, 'wt', encoding='UTF-8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
