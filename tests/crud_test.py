
from storage.memory_store import (
    initialize_database,
    add_memory,
    get_memories,
    update_memory,
    delete_memory
)

from schemas.memory_candidate import MemoryCandidate

initialize_database()

user_id = "test_user_001"

candidate = MemoryCandidate(
    content="User prefers Python",
    category="preference",
    source="user_message",
    confidence=0.95
)

# CREATE
memory = add_memory(user_id, candidate)
print("CREATED:", memory.content)

# READ
memories = get_memories(user_id)
print("TOTAL MEMORIES:", len(memories))

# UPDATE
updated = update_memory(
    user_id,
    memory.id,
    "User now prefers Rust"
)
print("UPDATED:", updated)

# VERIFY UPDATE
for item in get_memories(user_id):
    if item.id == memory.id:
        print("NEW CONTENT:", item.content)

# DELETE
deleted = delete_memory(user_id, memory.id)
print("DELETED:", deleted)

# VERIFY DELETE
remaining_ids = {m.id for m in get_memories(user_id)}
print("MEMORY REMOVED:", memory.id not in remaining_ids)
