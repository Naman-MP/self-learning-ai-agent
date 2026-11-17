
from storage.memory_store import initialize_database, add_memory
from schemas.memory_candidate import MemoryCandidate

initialize_database()

candidate = MemoryCandidate(
    content="User prefers Python over JavaScript",
    category="preference",
    source="user_message",
    confidence=0.95
)

saved_memory = add_memory(
    user_id="test_user_001",
    candidate=candidate
)

print("Memory successfully saved!")
print(saved_memory.model_dump_json(indent=2))
