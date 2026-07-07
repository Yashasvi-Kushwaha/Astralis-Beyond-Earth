import faiss
import pickle
import numpy as np
from pathlib import Path


class VectorStore:

    def __init__(self, dimension=None):

        self.index = None
        self.metadata = []

        if dimension is not None:
            self.index = faiss.IndexFlatL2(dimension)

    def add(self, embeddings, metadata):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(embeddings)

        self.metadata.extend(metadata)

    def search(self, query_embedding, k=3):

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for distance, idx in zip(distances[0], indices[0]):

            if idx < len(self.metadata):

                results.append({
                    "distance": float(distance),
                    "metadata": self.metadata[idx]
                })

        return results

    # ----------------------------
    # Save FAISS index
    # ----------------------------

    def save(self, folder="vector_db"):

        folder = Path(folder)

        folder.mkdir(exist_ok=True)

        faiss.write_index(
            self.index,
            str(folder / "index.faiss")
        )

        with open(folder / "metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)

        print("Vector database saved.")

    # ----------------------------
    # Load FAISS index
    # ----------------------------

    def load(self, folder="vector_db"):

        folder = Path(folder)

        index_file = folder / "index.faiss"
        metadata_file = folder / "metadata.pkl"

        if not index_file.exists():
            return False

        if not metadata_file.exists():
            return False

        self.index = faiss.read_index(
            str(index_file)
        )

        with open(metadata_file, "rb") as f:
            self.metadata = pickle.load(f)

        print("Vector database loaded.")

        return True