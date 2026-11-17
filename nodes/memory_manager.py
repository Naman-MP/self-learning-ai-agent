from state.state import MemoryAgentState
from storage.memory_store import get_memories , add_memory , delete_memory , update_memory

def memory_manager(state: MemoryAgentState):
    memory_decisions = state.memory_decisions
    user_id = state.user_id
    memory_candidates = state.memory_candidates

    existing_memories = get_memories(user_id=user_id)
    existing_ids = {memory.id for memory in existing_memories}

    print("\n=== MEMORY DEBUG ===")

    print("Candidates:")
    for i, candidate in enumerate(state.memory_candidates):
        print(f"{i}: {candidate.content}")

    print("\nDecisions:")
    for decision in state.memory_decisions:
        print(decision.model_dump())

    print("====================\n")

    for decision in memory_decisions:
        index = decision.candidate_index

        if decision.action in ("ADD", "UPDATE"):
            if index is None or not (0 <= index < len(memory_candidates)):
                raise ValueError("Invalid candidate index")

        if decision.action in ("UPDATE", "DELETE"):
            if not decision.memory_id or decision.memory_id not in existing_ids:
                raise ValueError("Invalid memory ID or memory ownership")

        if decision.action == "UPDATE":
            if not decision.content or not decision.content.strip():
                raise ValueError("UPDATE requires non-empty content")

    # LOOP 2: EXECUTE DATABASE OPERATIONS
    operations_count = 0

    for decision in memory_decisions:

        if decision.action == "ADD":
            candidate = memory_candidates[decision.candidate_index]
            add_memory(user_id, candidate)
            operations_count += 1

        elif decision.action == "UPDATE":
            success = update_memory(
                user_id,
                decision.memory_id,
                decision.content
            )
            if not success:
                raise ValueError("Memory update failed")
            operations_count += 1

        elif decision.action == "DELETE":
            success = delete_memory(user_id, decision.memory_id)
            if not success:
                raise ValueError("Memory deletion failed")
            operations_count += 1

        elif decision.action == "IGNORE":
            continue

    return {"memory_operations_count": operations_count}
