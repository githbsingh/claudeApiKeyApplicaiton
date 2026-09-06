class TextChunker:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200
    ):

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str):

        chunks = []

        start = 0

        text_length = len(text)

        while start < text_length:

            end = start + self.chunk_size

            chunk = text[start:end]

            chunk = chunk.strip()

            if chunk:
                chunks.append(chunk)

            start = end - self.chunk_overlap

        return chunks