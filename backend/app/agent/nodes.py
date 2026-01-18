from app.agent.state import AgentState
from app.services.redis_cache import redis_cache
from app.services.vector_db import vector_db
from app.services.llm_factory import llm
from tavily import TavilyClient
from app.core.config import settings
from langchain_core.messages import SystemMessage, HumanMessage

tavily = TavilyClient(api_key=settings.TAVILY_API_KEY)

# check_cache_node is now in graph.py to control flow better, or we can keep it here.
# For circular imports, we moved check_cache to graph.py or we can keep imports clean.
# Let's keep specific nodes here.

def search_web_node(state: AgentState):
    """Perform live web search using Tavily."""
    query = state["topic"]
    if state.get("critique_comments"):
        query = f"{state['topic']} related to: {state['critique_comments']}"
        print(f"--- RE-SEARCHING WITH QUERY: {query} ---")

    # Enable Image Search
    results = tavily.search(query=query, max_results=3, search_depth="advanced", include_images=True)
    
    search_contents = [f"Content: {r['content']}\nSource: {r['url']}" for r in results.get("results", [])]
    images = results.get("images", []) # Tavily returns list of image URLs
    
    current_results = state.get("search_results") or []
    return {
        "search_results": current_results + search_contents,
        "images": images # Pass images to state
    }

def rag_node(state: AgentState):
    """Query Vector DB for PDF context."""
    vector_store = vector_db.get_vector_store()
    docs = vector_store.similarity_search(state["topic"], k=3)
    rag_contents = [f"Content: {doc.page_content}\nSource: {doc.metadata.get('source', 'Unknown')}" for doc in docs]
    return {"rag_data": rag_contents}

def write_node(state: AgentState):
    """Synthesize final report using LLM."""
    topic = state["topic"]
    web_data = "\n\n".join(state.get("search_results", []))
    pdf_data = "\n\n".join(state.get("rag_data", []))
    visual_data = "\n\n".join(state.get("visual_data", []))
    
    critique_prompt = ""
    if state.get("critique_comments"):
        critique_prompt = f"\n\nIMPORTANT: Previous Version was critiqued. Please address this feedback: {state['critique_comments']}"

    prompt = f"""You are a research assistant. 
    Topic: {topic}
    {critique_prompt}
    
    Using the following data, write a comprehensive Markdown report.
    
    --- WEB SEARCH DATA ---
    {web_data}
    
    --- INTERNAL DOCUMENTS (PDF RAG) ---
    {pdf_data}
    
    --- VISUAL ANALYSIS (Charts/Images) ---
    {visual_data}
    
    Report:"""
    
    messages = [
        SystemMessage(content="You are a helpful research assistant."),
        HumanMessage(content=prompt)
    ]
    
    response = llm.invoke(messages)
    final_report = response.content
    
    # Save to Redis Semantic Cache (Enterprise Feature)
    redis_cache.save(topic, final_report)
    
    return {"final_report": final_report}

def critique_node(state: AgentState):
    """Critique the draft report."""
    current_report = state.get("final_report")
    topic = state["topic"]
    
    current_rev = state.get("revision_number", 0)
    next_rev = current_rev + 1
    
    MAX_REVISIONS = 1 
    if next_rev > MAX_REVISIONS:
        return {"critique_comments": None, "revision_number": next_rev}

    prompt = f"""You are a critical editor.
    User Topic: {topic}
    
    Draft Report:
    {current_report}
    
    Does this report comprehensively answer the topic?
    If YES, return "ACCEPT".
    If NO, briefly describe what information is missing or needs improvement. Start with "REVISE: ".
    """
    
    messages = [HumanMessage(content=prompt)]
    response = llm.invoke(messages)
    feedback = response.content.strip()
    
    if "ACCEPT" in feedback:
        return {"critique_comments": None, "revision_number": next_rev}
    else:
        reason = feedback.replace("REVISE:", "").strip()
        return {"critique_comments": reason, "revision_number": next_rev}