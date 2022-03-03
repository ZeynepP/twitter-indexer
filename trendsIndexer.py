#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   @Author: zeynep pehlivan
   @Date: 02.03.2022

"""
import glob
from elasticsearch7 import Elasticsearch
import json
from utils import index, create_index



def index_all(es,path):
    files = glob.glob(path+"*.jsons")
    doc_list = []
    counter = 0
    for file in files:

        with open(file, 'r', encoding="utf-8") as f:

           for line in f:
                try:
                    jtweet = json.loads(line)

                    doc_list += extract(jtweet[2][0], jtweet[0])

                    counter = counter + 1
                    if counter > 100:
                        index(es, doc_list, index_name=INDEX_NAME)
                        doc_list = []
                        counter = 0
                except Exception as ex:
                    print(ex)
                    print(line) # there are lines with errors in folders like "Read timed out"

        print(counter)


def extract(trends, ts):
    doc_list = []
    as_of = trends["as_of"]
    created_at = trends["created_at"]
    timestamp = ts * 1000
    rank = 0
    for trend in trends["trends"]:
        temp= trend
        temp["as_of"] = as_of
        temp["created_at"] = created_at
        temp["timestamp"] = timestamp
        temp["rank"] = rank
        rank = rank +1

        doc_list.append(temp)


    return doc_list

HOME = "/usr/src/temp/"
#HOME = "./"
if __name__ == '__main__':
    es = Elasticsearch(['http://rex-gpu10.ina.fr:9200'])
    INDEX_NAME = "trends_2018"

    mapping = create_index(es,INDEX_NAME, HOME + "es-settings.json",HOME + "es-trends-mapping.json")
    index_all(es,HOME + "data/")
