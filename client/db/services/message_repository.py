
from datetime import datetime
from typing import Optional

from client.db.models.message import Message
from client.db.services.db_service import DatabaseService


class MessageRepository:
    def __init__(self, db:DatabaseService):
        self.db = db

    def create(self, message:Message):
        query = "INSERT INTO message (message_id, session_id, role, content, metadata, created_at) VALUES (:message_id, :session_id, :role, :content, :metadata, :created_at)"
        self.db.execute(query, message.model_dump())

    def delete_by_session_id(self, session_id:str):
        query = "DELETE FROM message WHERE session_id = ?"
        self.db.execute(query, (session_id,))

    def get_by_session_id(self, session_id:str) -> list[Optional[Message]]:
        query = "SELECT * FROM message WHERE session_id = ?"
        rows = self.db.get_all(query, (session_id,))
        return [Message(**row) for row in rows]

        