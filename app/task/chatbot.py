import pandas as pd

from app.task import Singleton
from app.task.sementic import EmbeddingModel
from app.task.keyword import KeywordModel


from app.config import paths

from app.utility.utils import ModelProcessor
from app.utility.rrf import RRF


class ComfortBot(metaclass=Singleton):
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.keyword_model = KeywordModel()
        self.df = pd.read_excel(paths.DATA_DIR.joinpath("comfort_datasets.xlsx"))

    def reply(self, query):
        query1_ids = self.embedding_model.search(query)
        query2_ids = self.keyword_model.serach(query)

        rrf_scores = RRF.get_rrf_scores(query1_ids, query2_ids)
        picked = ModelProcessor.top_k_sampling(rrf_scores["scores"][:3], weight=3)
        return self.df.loc[rrf_scores["ids"][picked]].answer
