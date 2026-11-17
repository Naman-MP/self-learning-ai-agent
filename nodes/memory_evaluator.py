from schemas.memory_decision import MemoryDecision
from state.state import MemoryAgentState
from pydantic import BaseModel , Field
from prompts.evaluator_prompt import evaluation_prompt
from llm import llm

class MemoryEvaluationResult(BaseModel):
    memory_decision: list[MemoryDecision] = Field(default_factory=list)

structured_llm = llm.with_structured_output(MemoryEvaluationResult, method='json_schema')
chain = evaluation_prompt | structured_llm

def memory_evaluator(state: MemoryAgentState):
    memory_candidates = state.memory_candidates
    retrieved_memories = state.retrieved_memories

    if not memory_candidates:
        return {"memory_decisions": []}


    indexed_candidates = [
    {
        "candidate_index": index,
        "content": candidate.content,
        "category": candidate.category,
        "source": candidate.source,
        "confidence": candidate.confidence
    }
    for index, candidate in enumerate(memory_candidates)
]

    response = chain.invoke({
        'memory_candidates':memory_candidates,
        'retrieved_memories': retrieved_memories
    })

    if isinstance(response, dict) and "parsed" in response:
        response = response["parsed"]

    if response is None:
        raise ValueError("Ollama returned no valid evaluation result")

    # Validate dictionaries or Pydantic objects
    validated_response = MemoryEvaluationResult.model_validate(response)

    return {'memory_decisions':validated_response.memory_decision}

