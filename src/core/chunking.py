from src.config.settings import VectorConfig

class TextChunker:
    def __init__(self):
        self.chunk_size = VectorConfig.CHUNK_SIZE
        self.overlap = VectorConfig.CHUNK_OVERLAP

    def chunk_text(self, text: str) -> list[str]:
        """Split text into overlapping chunks using sliding window"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start += self.chunk_size - self.overlap

            # Prevent infinite loop on very small texts
            if end >= len(text):
                break

        return chunks
