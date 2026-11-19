
import datetime
from typing import Optional

from client.db.models.session import Session
from client.db.services.db_service import DatabaseService


class SessionRepository:
    def __init__(self, db_service:DatabaseService):
        self.db_service = db_service

    def create(self, session:Session):
        session.created_at = datetime.now()
        query = "INSERT INTO sessions (session_id, title, status, created_at) VALUES (?, ?, ?, ?)"
        self.db_service.execute(query, tuple(session.model_dump().values()))

    def get_session(self, session_token: str) -> Optional[Session]:
        query = "SELECT * FROM sessions WHERE session_token = ?"
        row = self.db_service.get_one(query, (session_token,))
        return Session(**row) if row else None

    def delete_session(self, session_token: str):
        query = "DELETE FROM sessions WHERE session_token = ?"
        self.db_service.execute(query, (session_token,))