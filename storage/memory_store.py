import sqlite3 as sql
from uuid import uuid4
from datetime import datetime, timezone

from schemas.memory_candidate import MemoryCandidate
from state.state import MemoryRecord


def initialize_database():
    conn = sql.connect("agent_memory.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            source TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == "__main__":
    initialize_database()


def add_memory(user_id: str, candidate: MemoryCandidate) -> MemoryRecord:
    memory_id = str(uuid4())
    now = datetime.now(timezone.utc)

    conn = sql.connect("agent_memory.db")
    try:
        conn.execute(
            """
            INSERT INTO memories
            (id, user_id, content, category, source, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                memory_id,
                user_id,
                candidate.content,
                candidate.category,
                candidate.source,
                now.isoformat()
            )
        )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return MemoryRecord(
        id=memory_id,
        content=candidate.content,
        category=candidate.category,
        source=candidate.source,
        updated_at=now
    )



def get_memories(user_id: str) -> list[MemoryRecord]:
    conn = sql.connect("agent_memory.db")
    conn.row_factory = sql.Row

    try:
        cursor = conn.execute(
            """
            SELECT id, content, category, source, updated_at
            FROM memories
            WHERE user_id = ?
            ORDER BY updated_at DESC
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        memories = [
            MemoryRecord(
                id=row["id"],
                content=row["content"],
                category=row["category"],
                source=row["source"],
                updated_at=datetime.fromisoformat(row["updated_at"])
            )
            for row in rows
        ]

        return memories

    finally:
        conn.close()



def update_memory(
    user_id: str,
    memory_id: str,
    new_content: str
) -> bool:

    conn = sql.connect("agent_memory.db")

    try:
        cursor = conn.execute(
            """
            UPDATE memories
            SET content = ?, updated_at = ?
            WHERE id = ? AND user_id = ?
            """,
            (
                new_content,
                datetime.now(timezone.utc).isoformat(),
                memory_id,
                user_id
            )
        )

        conn.commit()
        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()



def delete_memory(user_id: str, memory_id: str) -> bool:

    conn = sql.connect("agent_memory.db")

    try:
        cursor = conn.execute(
            """
            DELETE FROM memories
            WHERE id = ? AND user_id = ?
            """,
            (memory_id, user_id)
        )

        conn.commit()
        return cursor.rowcount > 0

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
