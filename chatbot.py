import pandas as pd
import numpy as np
import faiss
import random
from sentence_transformers import SentenceTransformer

df = pd.read_excel("./data/base_datasets.xlsx")
embedder = SentenceTransformer("./models/Huffon_sentence-klue-roberta-base")
index = faiss.read_index("./faiss/sts.index")

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
    index_q = [i[1]for i in zip(distances[0], indices[0]) if i[0] <= THRESHOLD]

    if len(index_q) < 2:
        return df.loc[index_q[0]].system

    return df.loc[index_q[random.randint(0, 1)]].system

# print(chatbot_answer("사랑했던 사람이 떠났어"))
