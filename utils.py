import glob

from elasticsearch7 import helpers
import json



def create_index(es,index_name, settings_file, mapping_file):
    with open(mapping_file) as f:
        mapping = json.load(f)
    if not es.indices.exists(index=index_name):
        with open(settings_file) as f:
            settings = json.load(f)

        es.indices.create(index=index_name, settings =settings, mappings=mapping)

    return mapping

def index(es, doc_list, index_name):
    try:
        res = helpers.bulk(es, doc_list, index=index_name)
        print("indexing bulk data RESPONSE:", res)

    except Exception as e:
        print("ERROR helpers bulk: %s", e)

