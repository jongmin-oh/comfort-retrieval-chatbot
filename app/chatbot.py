import pandas as pd
import numpy as np
import faiss
import random
from pathlib import Path
from sentence_transformers import SentenceTransformer
from app.models import cnxpool

BASE_DIR = str(Path(__file__).resolve().parent)

embedder = SentenceTransformer(
    BASE_DIR + "/sbert_models/Huffon_sentence-klue-roberta-base")
index = faiss.read_index(BASE_DIR + "/faiss/sts.index")

THRESHOLD = 50
SEARCH_AMOUNT = 5


def chatbot_answer(query):
    # Retrieval part
    qestion_embedding = embedder.encode(query, convert_to_tensor=True)
    input_embedding = np.expand_dims(qestion_embedding, axis=0)
    distances, indices = index.search(input_embedding, SEARCH_AMOUNT)

    # max distance 가 임계치를 안넘으면 무슨말인지 모르겠어요 하고 NoSQL에 축적
    if np.min(distances[0]) > THRESHOLD:
        # print(np.max(distances[0]))
        return "무슨 말인지 잘 모르겠어요 다시 한 번 말씀해주시겠어요??"

    index_q = [i[1]
               for i in zip(distances[0], indices[0]) if i[0] <= THRESHOLD]
    index_q = list(map(lambda x: x+1, index_q))
    index_q = str(index_q).replace('[', '(').replace(']', ')')

    # MySQL DB에서 임베딩 벡터를 검색 Bi-Encoder
    cnx = cnxpool.get_connection()
    cursor = cnx.cursor(dictionary=True)

    sql = f"""SELECT `index` , `user`, `system` FROM chatbot_data WHERE `index` IN {index_q};"""
    cursor.execute(sql)
    res = cursor.fetchall()

    cnx.close()
    cursor.close()

    temp = pd.DataFrame(res)

    if len(temp) < 2:
        return temp.loc[0].system

    return temp.loc[random.randint(0, 1)].system

#print(chatbot_answer("사랑했던 사람이 떠났어"))
