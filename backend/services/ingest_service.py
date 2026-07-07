from pathlib import Path

from rag.loader import PDFLoader
from rag.chunker import TextChunker
from rag.embedder import Embedder
from rag.vector_store import VectorStore


class IngestService:

    def __init__(self):

        self.loader = PDFLoader()
        self.chunker = TextChunker()
        self.embedder = Embedder()

    def ingest(self, pdf_path: str):

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(pdf_path)

        # Load existing vector database
        vector_store = VectorStore()

        if not vector_store.load():
            raise RuntimeError("Vector database not found.")

        metadata = []

        pages = self.loader.load_pdf(pdf_path)

        for page in pages:

            chunks = self.chunker.chunk_text(page["text"])

            for chunk in chunks:

                metadata.append({
                    "paper": pdf_path.name,
                    "page": page["page"],
                    "text": chunk
                })

        texts = [
            item["text"]
            for item in metadata
        ]

        embeddings = self.embedder.embed(texts)

        vector_store.add(
            embeddings,
            metadata
        )

        vector_store.save()

        return {
            "paper": pdf_path.name,
            "chunks": len(metadata)
        }