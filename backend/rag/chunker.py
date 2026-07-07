class TextChunker:
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100):
        """
        Split text into overlapping word chunks.
        """
        words = text.split()
        chunks = []

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk = " ".join(words[start:end])
            chunks.append(chunk)

            start += chunk_size - overlap

        return chunks