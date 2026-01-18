from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "AMRI Research Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # LLM & Tools
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    
    # Databases
    REDIS_URL: str = "redis://redis:6379/0"
    QDRANT_URL: str = "http://qdrant:6333"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()