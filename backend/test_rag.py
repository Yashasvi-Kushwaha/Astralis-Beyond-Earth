from rag.loader import PDFLoader
from rag.chunker import TextChunker
from rag.embedder import Embedder
from rag.vector_store import VectorStore

# ------------------------
# Load paper
# ------------------------

loader = PDFLoader()

text = loader.load_pdf("data/papers/blackholes.pdf")

# ------------------------
# Chunk paper
# ------------------------

chunker = TextChunker()

chunks = chunker.chunk_text(text)

print(f"Chunks created: {len(chunks)}")

# ------------------------
# Create embeddings
# ------------------------

embedder = Embedder()

embeddings = embedder.embed(chunks)

print("Embedding shape:", embeddings.shape)

# ------------------------
# Create vector store
# ------------------------

vector_store = VectorStore(
    dimension=embeddings.shape[1]
)

vector_store.add(
    embeddings,
    chunks
)

print("Vector store created.")

# ------------------------
# Search
# ------------------------

query = "What is a black hole?"

query_embedding = embedder.embed([query])[0]

results = vector_store.search(
    query_embedding,
    k=3
)

print("\n========== SEARCH RESULTS ==========\n")

for i, chunk in enumerate(results, start=1):
    print(f"\n------ Result {i} ------\n")
    print(chunk[:500])