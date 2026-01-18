from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    topic: str
    enable_hitl: bool = False # Enable Human-in-the-Loop

class ResearchResponse(BaseModel):
    report: Optional[str] = None
    source: str
    thread_id: Optional[str] = None
    status: str = "completed" # completed, paused
