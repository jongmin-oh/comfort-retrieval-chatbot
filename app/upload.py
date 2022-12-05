import pandas as pd
from pathlib import Path
import os
import json
from elasticsearch import Elasticsearch, helpers
from config import ELASTIC_HOST

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = os.path.join(BASE_DIR,'data','base_datasets.xlsx')
MAPPING_PATH = os.path.join(BASE_DIR,'mapping.json')
MAPPING = json.load(open(MAPPING_PATH))

df = pd.read_excel(DATA_PATH)
df['idx'] = df.index

client = Elasticsearch(hosts=ELASTIC_HOST)

def filterKeys(document, use_these_keys):
    return {key: document[key] for key in use_these_keys}

# 해당 인덱스(유저)가 없으면 새로 생성
def doc_generator(df, index):
    df_iter = df.iterrows()
    cols = df.columns.to_list()
    temp = list()

    for idx, document in df_iter:
        temp.append(
            {
                "_index": index,
                "_id": f"{idx}",
                "_source": filterKeys(document, cols),
            }
        )
    return temp

def upload(df, index):
    client.indices.create(index=index, body=MAPPING)
    data = doc_generator(df, index)
    helpers.bulk(client, data)

upload(df,"chatbot")
client.close()