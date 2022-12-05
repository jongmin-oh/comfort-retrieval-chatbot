from elasticsearch import Elasticsearch
from app.config import ELASTIC_HOST

class ElasticSearch:
    def __init__(self):
        self.client = None

    def connect(self):
        self.client = Elasticsearch(hosts=ELASTIC_HOST)

    def close(self):
        self.client.close()


elastic = ElasticSearch()