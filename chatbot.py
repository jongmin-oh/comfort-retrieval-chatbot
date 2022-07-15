import pandas as pd
import numpy as np
import json
import faiss
from datetime import datetime
import random
from sentence_transformers import SentenceTransformer , util

import mysql.connector.pooling

#MySQL DB 연결
with open('./config/db_config.json','r') as f:
    dbconfig = json.load(f)
    
cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = 'mypool',
                                                      pool_size = 3,
                                                      pool_reset_session=True,
                                                      **dbconfig) 

qestion_embedder = SentenceTransformer("Huffon/sentence-klue-roberta-base")
index = faiss.read_index("./faiss/sts.index")

def chatbot_answer(query : str ) -> str :

    qestion_embedding = qestion_embedder.encode(query, normalize_embeddings=True,convert_to_tensor=True)
    distances, indices = index.search(np.expand_dims(qestion_embedding,axis=0),3)
    
    #max distance 가 0.5가 안넘으면 무슨말인지 모르겠어요 하고 NoSQL에 축적
    if np.min(distances[0]) > 0.6:
        #----NoSQL로 전송-------#
        #print(np.max(distances[0]))
        return "무슨 말인지 잘 모르겠어요 다시 한 번 말씀해주시겠어요??"
    
    index_q = [i[1] for i in zip(distances[0],indices[0]) if i[0] <= 0.6]
    index_q = list(map(lambda x : x+1, index_q))
    index_q = str(index_q).replace('[','(').replace(']',')')
    
    # MySQL DB에서 임베딩 벡터를 검색 Bi-Encoder
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(dictionary=True)
    
    sql = f"""SELECT `index` , user, system FROM chatbot WHERE `index` IN {index_q};"""
    cursor.execute(sql)
    res = cursor.fetchall()

    cnx.close()
    cursor.close()
    
    temp = pd.DataFrame(res)
    
    return temp.loc[random.randint(0,2)].system