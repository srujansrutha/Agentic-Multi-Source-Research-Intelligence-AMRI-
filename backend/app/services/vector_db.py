from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from langchain.docstore.document import Document
import uuid

class VectorDBService:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = "research_papers"
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure the collection exists."""
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config={"size": 1536, "distance": "Cosine"}
            )

    def get_vector_store(self):
        """Returns a LangChain Qdrant vector store object."""
        return Qdrant(
            client=self.client,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
        )

    def add_documents(self, documents: list[Document]):
        """Ingest documents into Qdrant."""
        vector_store = self.get_vector_store()
        vector_store.add_documents(documents)

# Global instance
vector_db = VectorDBService()
