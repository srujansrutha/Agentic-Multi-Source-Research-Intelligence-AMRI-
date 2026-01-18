from langchain_ollama import OllamaEmbeddings
from app.core.config import settings
from redis import Redis
import numpy as np
import json
import uuid

class RedisSemanticCache:
    def __init__(self, redis_url: str = settings.REDIS_URL, threshold: float = 0.15):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.threshold = threshold
        self.embeddings = OllamaEmbeddings(base_url=settings.OLLAMA_BASE_URL, model="qwen3-embedding:8b")
        self.index_name = "semantic-cache-index"
        self._create_index()

    def _create_index(self):
        """Create Redis Search Index for Vectors."""
        try:
            from redis.commands.search.field import VectorField, TextField
            from redis.commands.search.indexDefinition import IndexDefinition, IndexType
            
            # Check if index exists
            try:
                self.redis.ft(self.index_name).info()
            except:
                # Create Index
                schema = (
                    TextField("query"),
                    TextField("report"),
                    VectorField("vector",
                        "FLAT", {
                            "TYPE": "FLOAT32",
                            "DIM": 1536,
                            "DISTANCE_METRIC": "COSINE"
                        }
                    )
                )
                self.redis.ft(self.index_name).create_index(
                    schema,
                    definition=IndexDefinition(prefix=["cache:"], index_type=IndexType.HASH)
                )
        except Exception as e:
            print(f"Index creation failed or skipped: {e}")
    def lookup(self, query: str):
        """Find semantically similar query."""
        try:
            vector = self.embeddings.embed_query(query)
            # Simple vector search using Redis Stack
            # Note: For strict correctness we use KNN, but here we do a quick check
            from redis.commands.search.query import Query
            
            q = Query(f"*=>[KNN 1 @vector $vec AS score]").return_fields("report", "score").dialect(2)
            params = {"vec": np.array(vector, dtype=np.float32).tobytes()}
            
            results = self.redis.ft(self.index_name).search(q, query_params=params)
            
            if results.docs:
                doc = results.docs[0]
                # Redis score is distance (0 is identical, 1 is opposite)
                # Lower is better. 0.1 means very close.
                score = float(doc.score)
                if score < self.threshold:
                    return doc.report
            return None
        except Exception as e:
            print(f"Cache lookup failed: {e}")
            return None

    def save(self, query: str, report: str):
        """Save query and report."""
        try:
            vector = self.embeddings.embed_query(query)
            key = f"cache:{uuid.uuid4()}"
            self.redis.hset(key, mapping={
                "query": query,
                "report": report,
                "vector": np.array(vector, dtype=np.float32).tobytes()
            })
            # Set TTL 24 hours
            self.redis.expire(key, 86400) 
        except Exception as e:
            print(f"Cache save failed: {e}")

# Global Instance
redis_cache = RedisSemanticCache()
