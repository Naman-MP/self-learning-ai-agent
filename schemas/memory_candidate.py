from pydantic import BaseModel , Field
from typing import Literal


class MemoryCandidate(BaseModel):
    content: str
    category: Literal["preference", "goal", "fact", "progress"]
    source: str
    confidence: float = Field(ge=0.0 , le=1.0)