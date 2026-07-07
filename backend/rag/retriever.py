from rag.embedder import Embedder
from rag.reranker import Reranker
from rag.pipeline import vector_store, bm25_store
from rag.rrf import ReciprocalRankFusion

class Retriever:

    def __init__(self):

        self.vector_store = vector_store
        self.bm25_store = bm25_store
        self.rrf = ReciprocalRankFusion()
        self.embedder = Embedder()
        self.reranker = Reranker()

    def retrieve(self, query, k=5):

        # Semantic Search
        query_embedding = self.embedder.embed([query])[0]

        faiss_results = self.vector_store.search(
            query_embedding,
            k=50
        )

        # Keyword Search
        bm25_results = self.bm25_store.search(
            query,
            k=50
        )

        # Merge results
        merged = {}

        for item in faiss_results:

            key = (
                item["metadata"]["paper"],
                item["metadata"]["page"],
                item["metadata"]["text"]
            )

            merged[key] = item

        for item in bm25_results:

            key = (
                item["metadata"]["paper"],
                item["metadata"]["page"],
                item["metadata"]["text"]
            )

            if key not in merged:

                item["distance"] = 9999.0

                merged[key] = item

        candidates = list(merged.values())

        print(f"Hybrid candidates: {len(candidates)}")

        results = self.reranker.rerank(
            query,
            candidates,
            top_k=k
        )

        return results