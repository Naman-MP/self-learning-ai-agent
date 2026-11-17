
from storage.memory_store import initialize_database, get_memories

if __name__ == "__main__":
    initialize_database()

    user_id = "test_user_001"

    memories = get_memories(user_id)

    print(f"Found {len(memories)} memories for {user_id}")

    for memory in memories:
        print(memory.model_dump_json(indent=2))
