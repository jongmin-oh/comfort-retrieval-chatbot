import random
from app.connection import elastic
import requests
from app.config import PINGPONG_API_KEY , PINGPONG_URL , INDEX_NAME
from app.utils import jaccard_similarity , analyzer, insert_data

def ping_pong_reply(question):
    url = PINGPONG_URL + "10"
    data = {"request": {"query": f"{question}"}}
    header = {"Authorization": f"{PINGPONG_API_KEY}"}
    res = requests.post(url=url ,headers=header, json=data).json()
    return res['response']['replies'][0]['text']

def search_reply(question):
    query ={"match": {"user.nori": f"{question}"}}
    res = elastic.client.search(index=INDEX_NAME,query=query,source=['user','system'],size=5)
    user = [ i['_source']['user'] for i in res['hits']['hits']]
    systems = [ i['_source']['system'] for i in res['hits']['hits']]
    question_analyze = analyzer(question)
    sim_scores = [ jaccard_similarity(question_analyze , analyzer(i)) for i in user ]
    
    if max(sim_scores) <= 0.5:
        answer = ping_pong_reply(question)
        insert_data(question, answer, "generate")
        return ping_pong_reply(question)
    
    answers = [ i[0] for i in zip(systems,sim_scores) if i[1] > 0.5]
    top = random.choice(answers).replace("00","선생")
    return top


if __name__ == "__main__":
    elastic.connect()
    print(search_reply("집가서 뭐하지.."))
    elastic.close()