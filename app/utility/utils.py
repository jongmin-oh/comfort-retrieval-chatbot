import random
import re
from typing import List

import numpy as np
def clean(text: str):
    jamo_patterns = "([ㄱ-ㅎㅏ-ㅣ]+)"  # 한글 단일 자음&모음제거
    english_patterns = "[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]"
    special_patterns = "[-=+,#/\:$. @*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`'…》.!?]"  # 공백 특수문자 제거
    text = re.sub(pattern=jamo_patterns, repl="", string=text)
    text = re.sub(pattern=special_patterns, repl="", string=text)
    text = re.sub(pattern=english_patterns, repl="", string=text)
    text = re.sub(r"[0-9]+", "", string=text)
    text = text.replace("~", "")
    text = text.strip()
    return text


class ModelProcessor:
    @classmethod
    def mean_pooling(cls, model_output, attention_mask):
        model_output = model_output[0]
        token_embeddings = model_output
        input_mask_expanded = np.expand_dims(
            attention_mask, axis=-1
        )  # Expand dimensions
        input_mask_expanded = np.broadcast_to(
            input_mask_expanded, token_embeddings.shape
        )  # Broadcast to match token_embeddings shape
        sum_embeddings = np.sum(token_embeddings * input_mask_expanded, axis=1)
        sum_mask = np.clip(np.sum(input_mask_expanded, axis=1), a_min=1e-9, a_max=None)
        return sum_embeddings / sum_mask, input_mask_expanded, sum_mask
    @classmethod
    def softmax(cls, x):
        f_x = np.exp(x) / np.sum(np.exp(x))
        return f_x

    @classmethod
    def top_k_sampling(cls, score_list: List[int], weight: int = 1):
        score_list = [i * weight for i in score_list]
        softmax_list = ModelProcessor.softmax(score_list)
        pick = random.choices(range(len(score_list)), weights=softmax_list)
        return pick[0]
