from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from app.core.config import settings
from typing import Optional
import uuid

class VectorDBService:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = "research_papers"
        self.cache_collection = "semantic_cache"
        self.embeddings = OllamaEmbeddings(base_url=settings.OLLAMA_BASE_URL, model="qwen3-embedding:8b")
        self._ensure_collections()

    def _ensure_collections(self):
        """Ensure the collections exist."""
        for col in [self.collection_name, self.cache_collection]:
            if not self.client.collection_exists(col):
                self.client.create_collection(
                    collection_name=col,
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

    def search_cache(self, query: str, threshold: float = 0.9) -> Optional[str]:
        """Check for semantically similar past queries."""
        vector = self.embeddings.embed_query(query)
        results = self.client.search(
            collection_name=self.cache_collection,
            query_vector=vector,
            limit=1
        )
        if results and results[0].score >= threshold:
            print(f"--- SEMANTIC CACHE HIT: Score {results[0].score} ---")
            return results[0].payload.get("report")
        return None

    def save_to_cache(self, query: str, report: str):
        """Save query and report to semantic cache."""
        vector = self.embeddings.embed_query(query)
        point_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, query))
        self.client.upsert(
            collection_name=self.cache_collection,
            points=[{
                "id": point_id,
                "vector": vector,
                "payload": {"query": query, "report": report}
            }]
        )

# Global instance
vector_db = VectorDBService()
