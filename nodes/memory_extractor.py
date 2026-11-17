from state.state import MemoryAgentState
from schemas.memory_candidate import MemoryCandidate
from pydantic import BaseModel,Field
from llm import llm
from prompts.extraction_prompt import extraction_prompt

class ExtractionResult(BaseModel):
    memory_candidates: list[MemoryCandidate] = Field(default_factory=list)


structured_llm = llm.with_structured_output(ExtractionResult , method="json_schema")
chain = extraction_prompt | structured_llm


def memory_extractor(state: MemoryAgentState):
    messages = state.messages

    response = chain.invoke({"user_message":messages})

    return {"memory_candidates":response.memory_candidates}