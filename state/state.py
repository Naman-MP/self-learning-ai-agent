from pydantic import BaseModel , Field
from datetime import datetime
from langchain_core.messages import AnyMessage
from typing import Literal
from schemas.memory_candidate import MemoryCandidate
from schemas.memory_decision import MemoryDecision

class MemoryRecord(BaseModel):
    id: str
    content: str
    category: str
    source: str
    updated_at: datetime = Field(default_factory=datetime.now)



class MemoryAgentState(BaseModel):
    messages: list[AnyMessage] = Field(default_factory=list)
    user_id: str
    retrieved_memories: list[MemoryRecord] = Field(default_factory=list)
    memory_candidates: list[MemoryCandidate] = Field(default_factory=list)
    memory_decisions: list[MemoryDecision] = Field(default_factory=list)
    final_response: str = ""
    memory_operations_count: int = 0
    


