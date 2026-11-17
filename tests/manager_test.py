
from uuid import uuid4

from langchain_core.messages import HumanMessage

from schemas.memory_candidate import MemoryCandidate
from schemas.memory_decision import MemoryDecision
from state.state import MemoryAgentState
from nodes.memory_manager import memory_manager
from storage.memory_store import (
    initialize_database,
    add_memory,
    get_memories,
    delete_memory,
)


def make_candidate(content):
    return MemoryCandidate(
        content=content,
        category="preference",
        source="user_message",
        confidence=0.95
    )


def make_state(user_id, candidates=None, decisions=None):
    return MemoryAgentState(
        user_id=user_id,
        messages=[HumanMessage(content="Test memory manager")],
        memory_candidates=candidates or [],
        memory_decisions=decisions or [],
        final_response=""
    )


def run_tests():
    initialize_database()

    # Unique user prevents interference with previous tests
    user_id = f"test_{uuid4()}"

    try:
        # TEST 1: ADD
        print("\n========== TEST 1: ADD ==========")

        state = make_state(
            user_id,
            candidates=[make_candidate("User prefers Python")],
            decisions=[
                MemoryDecision(
                    action="ADD",
                    candidate_index=0,
                    content="User prefers Python",
                    reason="New preference"
                )
            ]
        )

        result = memory_manager(state)
        memories = get_memories(user_id)

        assert len(memories) == 1
        assert memories[0].content == "User prefers Python"
        assert result["memory_operations_count"] == 1

        memory_id = memories[0].id
        print("PASS: Memory added successfully")

        # TEST 2: IGNORE
        print("\n========== TEST 2: IGNORE ==========")

        state = make_state(
            user_id,
            candidates=[make_candidate("User prefers Python")],
            decisions=[
                MemoryDecision(
                    action="IGNORE",
                    candidate_index=0,
                    reason="Duplicate memory"
                )
            ]
        )

        result = memory_manager(state)

        assert len(get_memories(user_id)) == 1
        assert result["memory_operations_count"] == 0

        print("PASS: Duplicate ignored")

        # TEST 3: UPDATE
        print("\n========== TEST 3: UPDATE ==========")

        state = make_state(
            user_id,
            candidates=[make_candidate("User prefers Rust")],
            decisions=[
                MemoryDecision(
                    action="UPDATE",
                    candidate_index=0,
                    memory_id=memory_id,
                    content="User prefers Rust",
                    reason="Preference changed"
                )
            ]
        )

        result = memory_manager(state)
        memories = get_memories(user_id)

        assert len(memories) == 1
        assert memories[0].content == "User prefers Rust"
        assert result["memory_operations_count"] == 1

        print("PASS: Memory updated successfully")

        # TEST 4: INVALID INDEX
        print("\n========== TEST 4: INVALID INDEX ==========")

        state = make_state(
            user_id,
            candidates=[make_candidate("User likes AI")],
            decisions=[
                MemoryDecision(
                    action="ADD",
                    candidate_index=99,
                    content="User likes AI",
                    reason="New fact"
                )
            ]
        )

        try:
            memory_manager(state)
            raise AssertionError("Expected ValueError")
        except ValueError:
            assert len(get_memories(user_id)) == 1
            print("PASS: Invalid index rejected")

        # TEST 5: CROSS-USER SECURITY
        print("\n========== TEST 5: USER ISOLATION ==========")

        other_user_id = f"other_{uuid4()}"
        other_memory = add_memory(
            other_user_id,
            make_candidate("Other user prefers JavaScript")
        )

        state = make_state(
            user_id,
            decisions=[
                MemoryDecision(
                    action="DELETE",
                    memory_id=other_memory.id,
                    reason="Attempt to delete another user's memory"
                )
            ]
        )

        try:
            memory_manager(state)
            raise AssertionError("Expected ValueError")
        except ValueError:
            assert any(
                m.id == other_memory.id
                for m in get_memories(other_user_id)
            )
            print("PASS: Cross-user deletion blocked")

        # TEST 6: DELETE
        print("\n========== TEST 6: DELETE ==========")

        state = make_state(
            user_id,
            decisions=[
                MemoryDecision(
                    action="DELETE",
                    memory_id=memory_id,
                    reason="Explicit forget request"
                )
            ]
        )

        result = memory_manager(state)

        assert len(get_memories(user_id)) == 0
        assert result["memory_operations_count"] == 1

        print("PASS: Memory deleted successfully")

        # TEST 7: EMPTY DECISIONS
        print("\n========== TEST 7: EMPTY ==========")

        result = memory_manager(make_state(user_id))

        assert result["memory_operations_count"] == 0
        print("PASS: Empty decisions handled")

        print("\nALL 7 MEMORY MANAGER TESTS PASSED!")

    finally:
        # Clean up test data, even if an assertion fails
        for memory in get_memories(user_id):
            delete_memory(user_id, memory.id)

        if "other_user_id" in locals():
            for memory in get_memories(other_user_id):
                delete_memory(other_user_id, memory.id)


if __name__ == "__main__":
    run_tests()
