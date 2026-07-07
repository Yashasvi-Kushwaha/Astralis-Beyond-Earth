from pathlib import Path

from rag.loader import PDFLoader
from rag.chunker import TextChunker
from rag.embedder import Embedder
from rag.vector_store import VectorStore
from rag.bm25_store import BM25Store


loader = PDFLoader()
chunker = TextChunker()
embedder = Embedder()

vector_store = VectorStore()
bm25_store = BM25Store()

papers_folder = Path("data/papers")

all_metadata = []

for pdf in papers_folder.glob("*.pdf"):

    print(f"Loading {pdf.name}")

    pages = loader.load_pdf(pdf)

    for page in pages:

        chunks = chunker.chunk_text(page["text"])

        for chunk in chunks:

            all_metadata.append({
                "paper": pdf.name,
                "page": page["page"],
                "text": chunk
            })

bm25_store.build(all_metadata)

loaded = vector_store.load()

if loaded:

    print("Using existing vector database.")

else:

    print("Building vector database...")

    texts = [item["text"] for item in all_metadata]

    embeddings = embedder.embed(texts)

    vector_store = VectorStore(embeddings.shape[1])

    vector_store.add(embeddings, all_metadata)

    vector_store.save()

    print("Vector database created successfully.")