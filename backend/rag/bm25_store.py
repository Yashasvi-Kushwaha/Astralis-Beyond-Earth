from rank_bm25 import BM25Okapi
import numpy as np


class BM25Store:

    def __init__(self):
        self.bm25 = None
        self.documents = []

    def build(self, metadata):

        self.documents = metadata

        corpus = [
            doc["text"].lower().split()
            for doc in metadata
        ]

        self.bm25 = BM25Okapi(corpus)

        print("BM25 index created.")

    def search(self, query, k=10):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        indices = np.argsort(scores)[::-1][:k]

        results = []

        for idx in indices:

            results.append({

                "score": float(scores[idx]),

                "metadata": self.documents[idx]

            })

        return results