import pickle

import numpy as np
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords

from app.config import paths

stopwords = Stopwords()


class KeywordModel:
    def __init__(self):
        self.kiwi = Kiwi()
        self.bm25_path = paths.BM25_DIR.joinpath("bm25model")
        self.bm25_model = pickle.load(open(self.bm25_path, "rb"))

    def tokenize(self, text):
        tokens = self.kiwi.tokenize(text, stopwords=stopwords)
        return [(pos.form, pos.tag) for pos in tokens]

    def serach(self, query):
        tokenized_query = self.tokenize(query)
        scores = self.bm25_model.get_scores(tokenized_query)
        top_k_indices = np.argsort(scores)[-5:]
        return top_k_indices[::-1].tolist()
