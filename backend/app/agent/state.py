from typing import TypedDict, List, Optional

class AgentState(TypedDict):
    topic: str
    search_results: List[str]
    rag_data: List[str]
    final_report: Optional[str]
    source: Optional[str] # "cache" or "live"
    critique_comments: Optional[str]
    revision_number: int
    human_feedback: Optional[str] # For HITL
    enable_hitl: bool # Configuration flag
    visual_data: Optional[List[str]] # Image analysis/descriptions
    images: Optional[List[str]] # Raw Image URLs