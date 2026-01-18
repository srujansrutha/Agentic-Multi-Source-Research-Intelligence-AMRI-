from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    topic: str
    search_results: List[str]
    rag_data: List[str]
    final_report: Optional[str]
    source: Optional[str] # "cache" or "live"