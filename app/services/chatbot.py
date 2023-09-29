from typing import List, Tuple, Final

import numpy as np
import chromadb
from onnxruntime import InferenceSession
from transformers import AutoTokenizer

from app.config import paths
from app.utility.utils import mean_pooling, clean
from app.services import Singleton


class ComfortBot(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.base_model = "snunlp/KR-SBERT-V40K-klueNLI-augSTS"
        self.onnx_path = paths.MODEL_DIR.joinpath("sbert-model_uint8.onnx")
        self.sess = InferenceSession(
            str(self.onnx_path), providers=["CPUExecutionProvider"]
        )
        self.chroma_client = chromadb.PersistentClient()
        self.collection = self.chroma_client.get_collection("answers")
        self.tokenizer = AutoTokenizer.from_pretrained(self.base_model)
        self._THREADHOLD: Final[int] = 0.8

    def encode(self, query: str, normalize_embeddings=False) -> np.ndarray:
        # user turn sequence to query embedding
        model_inputs = self.tokenizer(query, return_tensors="pt")
        inputs_onnx = {k: v.cpu().detach().numpy() for k, v in model_inputs.items()}
        sequence = self.sess.run(None, inputs_onnx)
        query_embedding = mean_pooling(sequence, inputs_onnx["attention_mask"])[0][0]

        if normalize_embeddings:
            query_embedding = query_embedding / np.linalg.norm(query_embedding)

        return query_embedding

    def reply(self, query: str) -> str:
        cleaned = clean(query)
        if cleaned == "":
            return "헤헤..."

        query_embedding = self.encode(query, normalize_embeddings=True).tolist()
        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=1,
        )

        return result["metadatas"][0][0]["answer"]


if __name__ == "__main__":
    bot = ComfortBot()
    print(bot.reply("너 누구야??"))
