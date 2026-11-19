
from datetime import datetime
from typing import Optional

from client.db.models.message import Message
from client.db.services.db_service import DatabaseService


class MessageRepository:
    def __init__(self, db:DatabaseService):
        self.db = db

    def create(self, message:Message):
        message.created_at = datetime.now()
        query = "INSERT INTO messages (message_id, session_id, role, content, metadata, created_at) VALUES (?, ?, ?, ?, ?, ?)"
        self.db.execute(query, tuple(message.model_dump().values()))

    def get_by_session_id(self, session_id:str) -> list[Optional[Message]]:
        query = "SELECT * FROM messages WHERE session_id = ?"
        rows = self.db.get_all(query, (session_id,))
        return [Message(**row) for row in rows]

        