from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import check_cache_node, search_web_node, rag_node, write_node

def create_graph():
    graph = StateGraph(AgentState)

    graph.add_node("check_cache", check_cache_node)
    graph.add_node("search_web", search_web_node)
    graph.add_node("rag", rag_node)
    graph.add_node("write", write_node)

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

    graph.add_edge("search_web", "rag")
    graph.add_edge("rag", "write")
    graph.add_edge("write", END)

    return graph.compile()

graph_app = create_graph()