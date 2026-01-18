from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings


class LLMFactory:
    @staticmethod
    def create_llm(model_name: str = None):
        """
        Creates a Model-Agnostic LLM interface.
        Switch between Gemini (Cloud) and Ollama (Local/GPU) via env vars.
        """
        if settings.LLM_PROVIDER == "ollama":
            # Use model from env or default to mistral:7b
            local_model = model_name or getattr(settings, 'OLLAMA_MODEL', 'mistral:7b')
            return ChatOllama(
                base_url=settings.OLLAMA_BASE_URL,
                model=local_model,
                temperature=0
            )
        
        # Default to Gemini
        return ChatGoogleGenerativeAI(
            model=model_name or "gemini-2.0-flash",
            temperature=0,
            google_api_key=settings.GEMINI_API_KEY
        )

llm = LLMFactory.create_llm()
