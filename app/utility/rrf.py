from app.config import Parms


class RRF:
    def get_ranking(query1_ids, query2_ids):
        # 중복 없는 모든 값들을 구합니다.
        all_values = list(set(query1_ids + query2_ids))

        # 결과를 저장할 딕셔너리를 초기화합니다.
        ranking = {}

        # 모든 값을 순회하면서 해당 값의 순위를 구합니다.
        for value in all_values:
            rank1 = query1_ids.index(value) + 1 if value in query1_ids else None
            rank2 = query2_ids.index(value) + 1 if value in query2_ids else None
            ranking[value] = [rank1, rank2]

        return ranking

    def reciprocal_rank(rank):
        """주어진 순위에 대한 Reciprocal Rank를 계산하는 함수"""
        try:
            return 1 / rank
        except TypeError:
            return 0.0

    @staticmethod
    def get_rrf_scores(query1_ids, query2_ids):
        ranking = __class__.get_ranking(query1_ids, query2_ids)

        ids = []
        scores = []

        for key in ranking.keys():
            # 각 검색 시스템의 순위
            embed_rank = ranking[key][0]
            keyword_rank = ranking[key][1]

            # 각 검색 시스템의 Reciprocal Rank 계산
            embed_rr = __class__.reciprocal_rank(embed_rank)
            keyword_rr = __class__.reciprocal_rank(keyword_rank)

            # 가중치가 적용된 Reciprocal Rank 계산
            rrf = (Parms.EMBED_WEIGHT * embed_rr) + (Parms.KEYWORD_WEIGHT * keyword_rr)

            scores.append(rrf)
            ids.append(key)

        sorted_scores = sorted(scores, reverse=True)
        sorted_ids = [
            key for _, key in sorted(zip(scores, ranking.keys()), reverse=True)
        ]
        return {"ids": sorted_ids, "scores": sorted_scores}