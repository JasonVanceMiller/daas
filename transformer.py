#!.venv/bin/python

# Transformer.py
# Accepts html documents, and chunks them into paragraphs. The paragraphs are then embedded for NLQ search. 
# The paragraph and embedding are inserted as one document into /wiki

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

# HTML parsing
from bs4 import BeautifulSoup 

# Warning silencing (lmao)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.set_verbosity(logging.ERROR)

# Initalizing global resources

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)

print ("module %s loaded" % module_url)

class html_data_class:
    def __init__(self, title, tags, paragraphs):
        self.title     = title     
        self.tags      = tags      
        self.paragraphs = paragraphs      
    def print(self):
        print("####################")
        print(self.title)
        print(self.tags)
        print(self.paragraphs)
        print("")

# :----------------------------------------------------:
def insert_into_opensearch(html_data):
    # html_data.print()
    embeddings = embed(html_data.paragraphs)

    for i in range(len(html_data.paragraphs)):
        # chunking by paragraph
        paragraph = html_data.paragraphs[i]
        if (len(paragraph) < 20):
            # @Hack excluding dud paragraphs
            continue
        
        url = 'https://localhost:9201/wiki/_doc'
        headers = dict()
        headers["Content-Type"] = "application/json"
        
        payload = dict()
        payload["title"] = html_data.title
        payload["tags"] = html_data.tags
        payload["paragraph"] = paragraph 
        payload["embedding"] = embeddings[i].numpy().tolist()
        payload["embedding_model"] = module_url 
        # @TODO 
        payload["paragraph_number"] = i + 1 
        payload["version"] = "0.1.0" 

        r = requests.post(url, data=json.dumps(payload), headers=headers, auth=("admin", "ChangeIt123!"), verify=False)
        if r.status_code != 200 and r.status_code != 201:
            print("Something went wrong in insert_into_nlq_search")
            print(r.status_code)
            print(r.content)
    return 

# :----------------------------------------------------:
def embed(input):
  return model(input)


# :----------------------------------------------------:
def title_from_html_cont(html_cont):
    soup = BeautifulSoup(html_cont, 'html.parser')
    return soup.title.get_text()
    

# :----------------------------------------------------:
def tags_from_html_cont(html_cont):
    # @TODO 
    return list()

# :----------------------------------------------------:
def paragraphs_from_html_cont(html_cont):
    soup = BeautifulSoup(html_cont, 'html.parser')

    # Extract text from nested tags
    p_tags = soup.find_all('p')  
    paragraphs = []
    for p in p_tags:
        paragraphs.append(p.get_text())
    return paragraphs


# :----------------------------------------------------:
def process_html_cont(html_cont):
    paragraphs = paragraphs_from_html_cont(html_cont)
    if len(paragraphs) == 0:
        # dud article
        return 
    title      = title_from_html_cont(html_cont)
    tags       = tags_from_html_cont(html_cont)

    print(title)
    
    html_data = html_data_class(title, tags, paragraphs)
    
    insert_into_opensearch(html_data)

# :----------------------------------------------------:
def main():
    path_list = Path("wikipedia_dump").glob('**/*') # */
    for path in path_list:
        file_name = str(path)
        if os.path.isdir(file_name):
            continue

        with open(file_name, 'r', encoding='utf-8') as file:
            try:
                html_cont = file.read()
                process_html_cont(html_cont)
            except Exception as e: 
               # print(e) #Printing mostly complaints about jpgs
               pass
    print("Done")

# :----------------------------------------------------:
if __name__ == "__main__":
    main()
