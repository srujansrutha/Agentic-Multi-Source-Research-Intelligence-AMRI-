from app.agent.state import AgentState
from app.services.redis_cache import redis_client
from app.services.vector_db import vector_db
from app.services.llm_factory import llm
from tavily import TavilyClient
from app.core.config import settings
from langchain_core.messages import SystemMessage, HumanMessage

tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

def check_cache_node(state: AgentState):
    """Check Redis for existing report on this topic."""
    cached_result = redis_client.get_cache(state["topic"])
    if cached_result:
        return {
            "final_report": cached_result.get("report"),
            "source": "cache"
        }
    return {"source": "live"}

def search_web_node(state: AgentState):
    """Perform live web search using Tavily."""
    # Skip if we already found it in cache
    if state.get("source") == "cache":
        return {}
        
    query = state["topic"]
    results = tavily.search(query=query, max_results=3, search_depth="advanced")
    
    # Store just the content strings or minimal summaries
    search_contents = [r["content"] for r in results.get("results", [])]
    return {"search_results": search_contents}

def rag_node(state: AgentState):
    """Query Vector DB for PDF context."""
    if state.get("source") == "cache":
        return {}
    
    vector_store = vector_db.get_vector_store()
    # Simple similarity search
    docs = vector_store.similarity_search(state["topic"], k=3)
    rag_contents = [doc.page_content for doc in docs]
    return {"rag_data": rag_contents}

def write_node(state: AgentState):
    """Synthesize final report using LLM."""
    if state.get("source") == "cache":
        return {}

    topic = state["topic"]
    web_data = "\n\n".join(state.get("search_results", []))
    pdf_data = "\n\n".join(state.get("rag_data", []))

    prompt = f"""You are a research assistant. 
    Topic: {topic}
    
    Using the following data, write a comprehensive Markdown report.
    
    --- WEB SEARCH DATA ---
    {web_data}
    
    --- INTERNAL DOCUMENTS (PDF RAG) ---
    {pdf_data}
    
    Report:"""
    
    messages = [
        SystemMessage(content="You are a helpful research assistant."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    final_report = response.content
    
    # Cache the result for future
    redis_client.set_cache(topic, {"report": final_report})
    
    return {"final_report": final_report}