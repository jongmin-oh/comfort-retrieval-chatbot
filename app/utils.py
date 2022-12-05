from app.connection import elastic
from app.config import INDEX_NAME

def analyzer(question):
    if elastic.client == None:
        elastic.connect()
    res = elastic.client.indices.analyze(index=INDEX_NAME,analyzer="nori_token_analyzer",text=question,
                                         attributes=["leftPOS"],
                                         explain=True)
    pos_tag = [(i['token'],i['leftPOS']) for i in res['detail']['tokenizer']['tokens'] if i['leftPOS'] != 'SP(Space)']
    return pos_tag

def jaccard_similarity(sentence1, sentence2):
    A = set(sentence1)
    B = set(sentence2)
    # Find intersection of two sets
    nominator = A.intersection(B)
    # Find union of two sets
    denominator = A.union(B)
    # Take the ratio of sizes
    similarity = len(nominator) / len(denominator)
    return similarity

def get_max_idx():
    body = {"sort": [{"idx": {"order": "desc"}}], "size": 1}
    res = elastic.client.search(index=INDEX_NAME, body=body)["hits"]["hits"][0]
    return res['_source']['idx']

def delete_indics():
    if elastic.client == None:
        elastic.connect()
    elastic.client.indices.delete(index=INDEX_NAME)

def insert_data(question, answer, type):
    idx = int(get_max_idx()) + 1
    doc = {
        "idx" : idx,
        "user" : question,
        "system" : answer,
        "sentiment" : type
    }
    elastic.client.index(index=INDEX_NAME,id=str(idx), body=doc)
    
def search_gererate():
    if elastic.client == None:
        elastic.connect()
    query ={"match": {"sentiment": f"generate"}}
    res = elastic.client.search(index=INDEX_NAME,query=query)
    return res