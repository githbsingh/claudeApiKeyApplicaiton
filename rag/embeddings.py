from sentence_transformers import SentenceTransformer


class EmbeddingService:

    def __init__(
        self,
        model_name="all-MiniLM-L6-v2"
    ):

        self.model = SentenceTransformer(
            model_name
        )

    def embed_documents(
        self,
        documents
    ):

        return self.model.encode(
            documents,
            normalize_embeddings=True
        )

    def embed_query(
        self,
        query
    ):

        return self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]