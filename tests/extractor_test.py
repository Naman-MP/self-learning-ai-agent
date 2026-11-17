
from langchain_core.messages import HumanMessage
from state.state import MemoryAgentState
from nodes.memory_extractor import memory_extractor
if __name__ == "__main__":

    test_queries = [
        "I prefer Python over JavaScript.",
        "I want to become an AI researcher.",
        "What is 5 + 5?",
        "I completed my LangGraph course.",
        "I'm learning LangGraph and prefer short explanations."
    ]

    for i, query in enumerate(test_queries, start=1):
        print(f"\n{'=' * 50}")
        print(f"TEST {i}: {query}")
        print("=" * 50)

        state = MemoryAgentState(
            user_id="test_user_001",
            messages=[HumanMessage(content=query)]
        )

        try:
            result = memory_extractor(state)

            candidates = result["memory_candidates"]

            print(f"Extracted memories: {len(candidates)}")

            for candidate in candidates:
                print(candidate.model_dump_json(indent=2))

            if not candidates:
                print("No memories extracted.")

        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {e}")
