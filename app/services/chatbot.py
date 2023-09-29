import numpy as np
from chromadb import PersistentClient
from onnxruntime import InferenceSession
from transformers import AutoTokenizer

from app.config import paths, Parms
from app.utility.utils import mean_pooling, clean, top_k_sampling
from app.services import Singleton


class ComfortBot(metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self.onnx_path = str(paths.MODEL_DIR.joinpath("sbert-model_uint8.onnx"))
        self.sess = InferenceSession(self.onnx_path, providers=["CPUExecutionProvider"])
        self.chroma_client = PersistentClient()
        self.collection = self.chroma_client.get_collection("answers")
        self.tokenizer = AutoTokenizer.from_pretrained(paths.MODEL_DIR)

    def encode(self, query: str, normalize_embeddings=False) -> np.ndarray:
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
            return Parms.EVASION_ANSWER

        query_embedding = self.encode(query, normalize_embeddings=True).tolist()
        response = self.collection.query(
            query_embeddings=query_embedding,
            n_results=5,
            include=["metadatas", "distances"],
        )

        res_scores = [1 - s for s in response["distances"][0]]
        res_answers = [a["answer"] for a in response["metadatas"][0]]

        exceeded_scores = []
        exceeded_answers = []
        for score, answer in zip(res_scores, res_answers):
            if score > Parms.THREADHOLD:
                exceeded_scores.append(score)
                exceeded_answers.append(answer)

        if len(exceeded_scores) == 0:
            return Parms.EVASION_ANSWER

        picked = top_k_sampling(exceeded_scores, weight=3)
        return exceeded_answers[picked]


if __name__ == "__main__":
    bot = ComfortBot()
    print(bot.reply("너 누구야??"))
