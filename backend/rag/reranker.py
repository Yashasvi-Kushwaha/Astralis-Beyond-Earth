from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):
        print("Loading reranker...")

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Reranker loaded.")

    def rerank(self, query, retrieved, top_k=5):

        # Create (query, document) pairs
        pairs = [
            (query, item["metadata"]["text"])
            for item in retrieved
        ]

        # Compute relevance scores
        scores = self.model.predict(pairs)

        # Sort by highest score
        ranked = sorted(
            zip(scores, retrieved),
            key=lambda x: x[0],
            reverse=True
        )

        results = []

        for score, item in ranked[:top_k]:

            results.append({
                "score": float(score),
                "distance": item["distance"],
                "metadata": item["metadata"]
            })

        return results