#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   @Author: zeynep pehlivan
   @Date: 02.03.2022

"""
import glob
from elasticsearch7 import Elasticsearch
import json
from dateutil import parser
import calendar

from utils import index, create_index



def index_all(path):
    files = glob.glob(path+"*.jsons")
    doc_list = []
    counter = 0
    for file in files:

        with open(file, 'r', encoding="utf-8") as f:

           for line in f:
                jtweet = json.loads(line)
                tweet = jtweet[2]
                if "id" in tweet:
                    extract(tweet,doc_list)
                    counter = counter + 1
                    if counter > 100:
                        index(es, doc_list, index_name=INDEX_NAME)
                        doc_list = []
                        counter = 0

        print(counter)


def extract_entities(tweet, name):
    list_tweets = []
    if ("entities" in tweet and name in tweet["entities"]):
        if (len(tweet["entities"][name]) > 0):
            l = tweet["entities"][name]

            for e in l:
                t = {}
                for x in required_keys[name]:
                    if x in e:
                        t[x] = e[x]
                list_tweets.append(t)

    elif ("extended_entities" in tweet and name in tweet["extended_entities"]):
        if (len(tweet["extended_entities"][name]) > 0):
            l = tweet["extended_entities"][name]
            for e in l:
                t={}
                for x in required_keys[name]:
                    if x in e:
                        t[x] = e[x]
                list_tweets.append(t)

    return list_tweets


def extract_fields(tweet, name, field):
    list_tweets = []
    if ("entities" in tweet):
        if (len(tweet["entities"][name]) > 0):
            l = tweet["entities"][name]

            for e in l:
                list_tweets.append(e[field])

    elif ("extended_entities" in tweet):
        if (len(tweet["extended_entities"][name]) > 0):
            l = tweet["extended_entities"][name]
            for e in l:
                list_tweets.append(e[field])

    return list(list_tweets)

def extract(tweet,doc_list):
    t={}
    for x in required_keys["all"]:
        if x in tweet:
            t[x] = tweet[x]
    t["link_twitter"] = "https://twitter.com/zpehlivan/status/" + t["id_str"]
    if not 'full_text' in t:
        t["full_text"] = t["text"]
    t["_id"] = t["id_str"]
    timestamp = calendar.timegm(parser.parse(t["created_at"]).timetuple())

    t['created_at_local'] = timestamp * 1000
    t['hashtags'] = extract_fields(tweet, "hashtags", "text")
    t['user_mentions'] = extract_entities(tweet, "user_mentions")
    t['urls'] = extract_fields(tweet, "urls", "expanded_url")
    t['media'] = extract_entities(tweet, "media")

    doc_list.append(t)
    if ("id" in tweet):
        if ("retweeted_status" in tweet):
            return extract(tweet["retweeted_status"],doc_list)

        if ("quoted_status" in tweet):
            return extract(tweet["quoted_status"],doc_list)


HOME = "/usr/src/temp/"
# HOME = "./" for local run

if __name__ == '__main__':
    es = Elasticsearch(['http://rex-gpu10.ina.fr:9200'])
    INDEX_NAME = "twitter_201803"

    mapping = create_index(es,INDEX_NAME, HOME + "es-settings.json",HOME + "es-mapping.json")
    global required_keys
    required_keys={}
    required_keys["all"] = list(mapping["properties"].keys())
    required_keys["user_mentions"] = list(mapping["properties"]["user_mentions"]["properties"].keys())
    required_keys["media"] = list(mapping["properties"]["media"]["properties"].keys())

    required_keys["all"].remove("link_twitter")
    required_keys["all"].remove("id")


    index_all(es,HOME + "data/")
