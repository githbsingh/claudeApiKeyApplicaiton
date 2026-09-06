from pathlib import Path

from rag.document_loader import DocumentLoader
from rag.chunker import TextChunker
from rag.embeddings import EmbeddingService
from rag.vector_store import VectorStore


class RAGService:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = TextChunker()

        self.embeddings = EmbeddingService()

        self.vector_store = VectorStore()

    def ingest(
        self,
        file_path: str
    ):

        text = self.loader.load(
            file_path
        )

        chunks = self.chunker.split(
            text
        )

        embeddings = (
            self.embeddings
            .embed_documents(chunks)
        )

        file_name = Path(
            file_path
        ).name

        metadatas = [
            {
                "source": file_name,
                "chunk": index
            }
            for index in range(
                len(chunks)
            )
        ]

        ids = [
            f"{file_name}-{index}"
            for index in range(
                len(chunks)
            )
        ]

        self.vector_store.add_documents(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

        return len(chunks)

    def retrieve(self, query, top_k=5):
        query_embedding = self.embeddings.embed_query(query)
        results = self.vector_store.search(
            query_embedding,
            top_k
            )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        retrieved_chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):
            retrieved_chunks.append({
                "text": document,
                "metadata": metadata,
                "distance": distance
            })

        return retrieved_chunks

    def build_prompt(self, question, retrieved_chunks):
        context = "\n\n".join(
            f"""
    --- DOCUMENT CHUNK {i + 1} ---
    {chunk["text"]}
    """
        for i, chunk in enumerate(retrieved_chunks)
    )

        return f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the information
provided in the DOCUMENT CONTEXT.

STRICT RULES:

1. Use ONLY the supplied document context.
2. Do NOT use your general knowledge.
3. Do NOT make assumptions.
4. Do NOT invent information.
5. If the answer is not present in the document context,
   respond exactly:

"I couldn't find this information in the uploaded document."

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""