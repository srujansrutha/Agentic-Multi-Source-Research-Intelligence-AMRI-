from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    topic: str

class ResearchResponse(BaseModel):
    report: str
    source: str
