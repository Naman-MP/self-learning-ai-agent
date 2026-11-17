from pydantic import BaseModel , Field , model_validator
from typing import Literal

class MemoryDecision(BaseModel):
    action: Literal["ADD","UPDATE","DELETE","IGNORE"]
    memory_id: str | None = None
    content: str | None = None
    reason: str 
    candidate_index: int | None = Field(default=None , ge=0)

    @model_validator(mode='after')
    def validate_decision(self):
        if self.action == "UPDATE":
            if not self.memory_id:
                raise ValueError("UPDATE requires memory_id")

            if not self.content or not self.content.strip():
                raise ValueError("UPDATE requires non-empty content")

        if self.action == "DELETE" and not self.memory_id:
            raise ValueError("DELETE requires memory_id")

        return self
    