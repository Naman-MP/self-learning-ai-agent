from langchain_core.messages import HumanMessage
from graph.graph import memory_graph
from storage.memory_store import initialize_database

def main():
    initialize_database()
    user_id = 'user_001'

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit' or user_input.lower() == 'quit':
            break

        if not user_input:
            continue

        result = memory_graph.invoke(
            {
                'user_id':user_id,
                'messages':[HumanMessage(content=user_input)],
                'final_response': ""
            }
        )
        print("\nAI:", result["final_response"])

        print("\nMemory operations:", result["memory_operations_count"])

        for decision in result["memory_decisions"]:
            print(f"Decision: {decision.action}")
            print(f"Reason: {decision.reason}")


if __name__ == '__main__':
    main()