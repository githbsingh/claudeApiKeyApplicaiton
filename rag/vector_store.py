import chromadb


class VectorStore:

    def __init__(
        self,
        persist_directory="./chroma_db"
    ):

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = (
            self.client.get_or_create_collection(
                name="enterprise_knowledge"
            )
        )

    def add_documents(
        self,
        documents,
        embeddings,
        metadatas,
        ids
    ):

        self.collection.add(
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )

    def search(
        self,
        embedding,
        top_k=5
    ):

        return self.collection.query(
        query_embeddings=[
            embedding.tolist()
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )