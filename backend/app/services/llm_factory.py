from langchain_openai import ChatOpenAI
from app.core.config import settings

class LLMFactory:
    @staticmethod
    def create_llm(model_name: str = "gpt-4o"):
        """Creates a generic LangChain LLM interface."""
        # For now, we default to OpenAI. 
        # Future extension: Add logic to switch to ChatOllama if model_name is significantly different or configured.
        return ChatOpenAI(
            model=model_name,
            temperature=0,
            openai_api_key=settings.OPENAI_API_KEY
        )

llm = LLMFactory.create_llm()
