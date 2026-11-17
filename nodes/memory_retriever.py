from state.state import MemoryAgentState
from storage.memory_store import add_memory , delete_memory , update_memory , get_memories

def memory_retriever(state: MemoryAgentState):
    user_id = state.user_id
    memory_decision = state.memory_decisions
    memory = get_memories(user_id=user_id)
    return {"retrieved_memories": memory}
