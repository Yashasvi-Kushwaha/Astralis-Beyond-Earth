from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Embedding model loaded.")

    def embed(self, texts):
        """
        Convert a list of text chunks into embeddings.
        """
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings