import pandas as pd
from app.config import INDEX_NAME , ELASTIC_HOST
from pathlib import Path
from elasticsearch import Elasticsearch
import os
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = os.path.join(BASE_DIR,'data') + '/'

def talk_restoration(origin=False):
    client = Elasticsearch(hosts=ELASTIC_HOST)
    talk_list = list()

    # 최대 100,000개 까지 가능
    for i in range(-1, 100000, 10000):
        body = {
            "size": 10000,
            "search_after": [str(i)],
            "sort": [
                {
                    "idx": {"order": "asc"},
                }
            ],
            "query": {"match": {"sentiment": "generate"}}
        }
        search = client.search(index=INDEX_NAME, body=body)
        count = search["hits"]["total"]["value"]
        docs = search["hits"]["hits"]

        data = [doc["_source"] for doc in docs]
        client.close()
        
        # 10,000개 이상 검색될 경우 최대 10,000개로 측정됨
        if count == 10000:
            talk_list.append(data)

        # 10,000개 이하일 경우
        elif count > 0 and count < 10000:
            talk_list.append(data)
            break
        # 아바타 검색결과가 없을 경우
        elif count == 0:
            return []

    # 2차원 리스트를 1차원으로 변경
    reuslt = sum(talk_list, [])
    
    QA_pair_df = pd.DataFrame(reuslt)

    # 카톡 원본으로 복원을 할 것인가 옵션체크
    if origin == False:
        return QA_pair_df
    elif origin == True:
        temp = list()
        for row in QA_pair_df.itertuples():
            chat1 = {"time": row[1], "text": row[2], "type": "Q"}
            chat2 = {"time": row[3], "text": row[4], "type": "A"}
            temp.append(chat1)
            temp.append(chat2)
        origin_df = pd.DataFrame(temp)
        return origin_df

if __name__ == "__main__":
    df = talk_restoration()
    df.to_excel(DATA_DIR + datetime.now().strftime('%Y-%m-%d_%H') + '.xlsx')