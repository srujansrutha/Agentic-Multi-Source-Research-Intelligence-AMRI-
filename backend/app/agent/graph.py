from langgraph.graph import StateGraph, END
from langgraph.checkpoint.redis import RedisSaver
from app.agent.state import AgentState
from app.agent.nodes import search_web_node, rag_node, write_node, critique_node
from app.agent.safety import guardrail_node
from app.agent.human import human_review_node
from app.agent.vision import vision_node
from app.services.redis_cache import redis_cache
from app.core.config import settings

def check_cache_node(state: AgentState):
    """Check Redis for semantically similar report."""
    cached_report = redis_cache.lookup(state["topic"])
    if cached_report:
        print("--- [CACHE HIT] Returning existing report ---")
        return {
            "final_report": cached_report,
            "source": "cache",
            "revision_number": 0
        }
    return {"source": "live", "revision_number": 0}

# Create Redis Checkpointer for Persistence
# Pass URL string directly
memory = RedisSaver(settings.REDIS_URL)

def create_graph():
    graph = StateGraph(AgentState)

    graph.add_node("check_cache", check_cache_node)
    graph.add_node("search_web", search_web_node)
    graph.add_node("rag", rag_node)
    graph.add_node("write", write_node)
    graph.add_node("critique", critique_node)
    graph.add_node("guardrails", guardrail_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("vision", vision_node)

    graph.set_entry_point("check_cache")

    def cache_router(state: AgentState):
        if state.get("source") == "cache":
            return "end"
        return "continue"

    graph.add_conditional_edges(
        "check_cache",
        cache_router,
        {
            "end": END,
            "continue": "search_web"
        }
    )

    # Vision Layer (Multi-Modal)
    # Search -> Vision -> RAG
    graph.add_edge("search_web", "vision")
    graph.add_edge("vision", "rag")
    
    # HITL Router
    def hitl_router(state: AgentState):
        # We need to know if HITL is enabled.
        # Ideally this is in 'state' or 'config'.
        # For simplicity, we'll check if a flag 'enable_hitl' is in state (we need to pass it)
        if state.get("enable_hitl"):
            return "human"
        return "auto"

    graph.add_conditional_edges(
        "rag",
        hitl_router,
        {
            "human": "human_review",
            "auto": "write"
        }
    )
    
    graph.add_edge("human_review", "write")
    graph.add_edge("write", "critique")

    def critique_router(state: AgentState):
        if state.get("critique_comments"):
            return "revise"
        return "accept"

    graph.add_conditional_edges(
        "critique",
        critique_router,
        {
            "revise": "search_web",
            "accept": "guardrails"
        }
    )
    
    graph.add_edge("guardrails", END)

    # Compile with interruption
    return graph.compile(
        checkpointer=memory,
        interrupt_before=["human_review"]
    )

graph_app = create_graph()
