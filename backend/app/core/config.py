from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AMRI Research Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # LLM & Tools
    LLM_PROVIDER: str = "gemini"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral:7b"
    GEMINI_API_KEY: str
    TAVILY_API_KEY: str
    
    # GPU Configuration
    GPU_ENABLED: bool = True
    CUDA_VISIBLE_DEVICES: str = "0"
    
    # Observability (LangSmith)
    LANGCHAIN_TRACING_V2: str = "false"
    LANGCHAIN_ENDPOINT: str = "https://api.smith.langchain.com"
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "amri-agent"
    
    # Databases
    REDIS_URL: str = "redis://redis:6379/0"
    QDRANT_URL: str = "http://qdrant:6333"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()
