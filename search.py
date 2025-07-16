#!.venv/bin/python

# curl -ku 'admin:ChangeIt123!' https://localhost:9201/wiki/_search -H "Content-Type: application/json" -d "{\"query\": {\"match\":{\"paragraph\": {\"query\": \"Michael\"}}}}"

# Search.py
# Accepts a search query, and takes flags specifying if you want traditional search or nlq search

from absl import logging

import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns
import requests
from pathlib import Path
import json
import click

# Warning silencing (lmao)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.set_verbosity(logging.ERROR)

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

print ("module %s loaded" % module_url)

def traditional_search(query):
    url = 'https://localhost:9201/wiki/_search'
    headers = dict()
    headers["Content-Type"] = "application/json"
    
    payload = {"query": {"multi_match":{"fields": ["title", "paragraph"], "query": query}}} 

    # Post requests for queries in OS because JavaScript compatibility
    r = requests.post(url, data=json.dumps(payload), headers=headers, auth=("admin", "ChangeIt123!"), verify=False)
    print(r.status_code)
    if (r.status_code == 200):
        resp = r.json()
        for hit in resp["hits"]["hits"]:
            source = hit["_source"]
            # print(source)
            print("####################")
            print(source["title"])
            print(source["paragraph"])
            print("")
    return 

def nlq_search(embedding):
    url = 'https://localhost:9201/wiki/_search'
    headers = dict()
    headers["Content-Type"] = "application/json"
    
    payload = {"query": {"knn":{"embedding": { "vector": embedding, "k": 10 }}}}

    # Post requests for queries in OS because JavaScript compatibility
    r = requests.post(url, data=json.dumps(payload), headers=headers, auth=("admin", "ChangeIt123!"), verify=False)
    print(r.status_code)
    if (r.status_code == 200):
        resp = r.json()
        for hit in resp["hits"]["hits"]:
            source = hit["_source"]
            # print(source)
            print("####################")
            print(source["title"])
            print(source["paragraph"])
            print("")
    else:
        print(r.content)
    return 

# :----------------------------------------------------:
def embed(input):
  return model(input)

# :----------------------------------------------------:
@click.command()
@click.option('--nlq', is_flag=True)
@click.option('--traditional', is_flag=True)
@click.argument('query')
def main(nlq, traditional, query):
    print('Start')
    if not nlq and not traditional:
        print("You need to speify one of --nlq or --traditional, so I know how you want to search.")
    if nlq and traditional:
        print("Only one of --nql or --traditional please")

    if traditional:
        print("Traditional search for " + query)
        traditional_search(query)
    if nlq:
        print("Nlq search for " + query)
        embedding = embed([query])[0].numpy().tolist()
        # print(embedding)
        # embedding = embed([query, "apple bottom jeans"])[0].numpy().tolist()
        # print(embedding)
        nlq_search(embedding)

if __name__ == '__main__':
    main()
