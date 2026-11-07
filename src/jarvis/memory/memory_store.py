"""
JARVIS Permanent Memory
Local SQLite conversation storage.
"""

import sqlite3
from contextlib import closing
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]

DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "jarvis_memory.db"


class MemoryStore:

    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(
            self.db_path,
            timeout=10
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        with closing(self._connect()) as connection:
            with connection:
                connection.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        conversation_id TEXT NOT NULL,
                        role TEXT NOT NULL
                            CHECK(role IN ('user', 'assistant')),
                        content TEXT NOT NULL,
                        created_at TEXT NOT NULL
                            DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                connection.execute("""
                    CREATE INDEX IF NOT EXISTS
                    idx_messages_conversation
                    ON messages(conversation_id, id)
                """)

    def save_message(self, conversation_id, role, content):

        conversation_id = conversation_id.strip()
        role = role.strip().lower()
        content = content.strip()

        if not conversation_id:
            raise ValueError("Conversation ID cannot be empty.")

        if role not in ("user", "assistant"):
            raise ValueError("Invalid message role.")

        if not content:
            raise ValueError("Message cannot be empty.")

        with closing(self._connect()) as connection:
            with connection:
                cursor = connection.execute(
                    """
                    INSERT INTO messages
                    (conversation_id, role, content)
                    VALUES (?, ?, ?)
                    """,
                    (conversation_id, role, content)
                )

                return cursor.lastrowid

    def load_messages(self, conversation_id, limit=20):

        if limit < 1 or limit > 500:
            raise ValueError("Limit must be between 1 and 500.")

        with closing(self._connect()) as connection:
            rows = connection.execute(
                """
                SELECT id, conversation_id, role,
                       content, created_at
                FROM messages
                WHERE conversation_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (conversation_id, limit)
            ).fetchall()

        return [dict(row) for row in reversed(rows)]

    def count_messages(self):

        with closing(self._connect()) as connection:
            result = connection.execute(
                "SELECT COUNT(*) FROM messages"
            ).fetchone()

        return result[0]