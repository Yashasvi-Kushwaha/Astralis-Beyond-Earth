from collections import defaultdict


class ReciprocalRankFusion:

    def fuse(self, faiss_results, bm25_results, k=60):

        scores = defaultdict(float)
        documents = {}

        # FAISS ranking
        for rank, item in enumerate(faiss_results):

            key = (
                item["metadata"]["paper"],
                item["metadata"]["page"],
                item["metadata"]["text"]
            )

            scores[key] += 1 / (k + rank)
            documents[key] = item

        # BM25 ranking
        for rank, item in enumerate(bm25_results):

            key = (
                item["metadata"]["paper"],
                item["metadata"]["page"],
                item["metadata"]["text"]
            )

            scores[key] += 1 / (k + rank)

            if key not in documents:
                item["distance"] = 9999
                documents[key] = item

        ranked = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for key, score in ranked:

            doc = documents[key]
            doc["rrf_score"] = score
            results.append(doc)

        return results