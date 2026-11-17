
from datetime import datetime

from schemas.memory_candidate import MemoryCandidate
from schemas.memory_decision import MemoryDecision
from state.state import MemoryAgentState , MemoryRecord
from nodes.memory_evaluator import memory_evaluator

from langchain_core.messages import HumanMessage


def make_memory(content, category="preference", memory_id="mem_001"):
    return MemoryRecord(
        id=memory_id,
        content=content,
        category=category,
        source="user_message",
        updated_at=datetime.now()
    )


def make_candidate(content, category="preference"):
    return MemoryCandidate(
        content=content,
        category=category,
        source="user_message",
        confidence=0.95
    )


if __name__ == "__main__":

    test_cases = [
        {
            "name": "ADD - New memory",
            "message": "I prefer Python.",
            "existing": [],
            "candidates": [
                make_candidate("User prefers Python")
            ],
            "expected": "ADD"
        },
        {
            "name": "IGNORE - Duplicate memory",
            "message": "I prefer Python.",
            "existing": [
                make_memory("User prefers Python")
            ],
            "candidates": [
                make_candidate("User prefers Python")
            ],
            "expected": "IGNORE"
        },
        {
            "name": "UPDATE - Changed preference",
            "message": "I now prefer Python over JavaScript.",
            "existing": [
                make_memory("User prefers JavaScript")
            ],
            "candidates": [
                make_candidate("User now prefers Python over JavaScript")
            ],
            "expected": "UPDATE"
        },
        {
            "name": "DELETE - Explicit forget request",
            "message": "Forget that I prefer Python.",
            "existing": [
                make_memory("User prefers Python")
            ],
            "candidates": [
                make_candidate(
                    "User explicitly requests deletion of their Python preference"
                )
            ],
            "expected": "DELETE"
        },
        {
            "name": "EMPTY - No candidates",
            "message": "Hello!",
            "existing": [],
            "candidates": [],
            "expected": None
        }
    ]

    for i, case in enumerate(test_cases, start=1):
        print(f"\n{'=' * 55}")
        print(f"TEST {i}: {case['name']}")
        print("=" * 55)

        state = MemoryAgentState(
            user_id="test_user_001",
            messages=[HumanMessage(content=case["message"])],
            retrieved_memories=case["existing"],
            memory_candidates=case["candidates"],
            final_response=""
        )

        try:
            result = memory_evaluator(state)
            decisions = result["memory_decisions"]

            print(f"Expected: {case['expected']}")
            print(f"Decisions returned: {len(decisions)}")

            for decision in decisions:
                print(decision.model_dump_json(indent=2))

            if case["expected"] is None:
                passed = len(decisions) == 0
            else:
                passed = (
                    len(decisions) == 1
                    and decisions[0].action == case["expected"]
                )

                if passed and case["expected"] in ("UPDATE", "DELETE"):
                    passed = decisions[0].memory_id == "mem_001"

            print(f"RESULT: {'PASS' if passed else 'FAIL'}")

        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
