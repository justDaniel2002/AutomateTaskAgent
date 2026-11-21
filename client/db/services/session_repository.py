
import datetime
from typing import Optional

from client.db.models.session import Session
from client.db.services.db_service import DatabaseService


class SessionRepository:
    def __init__(self, db:DatabaseService):
        self.db_service = db

    def create(self, session:Session):
        query = "INSERT INTO session (session_id, title, status, created_at) VALUES (:session_id, :title, :status, :created_at)"
        self.db_service.execute(query, session.model_dump())

    def get_by_id(self, session_id: str) -> Optional[Session]:
        query = "SELECT * FROM session WHERE session_id = ?"
        row = self.db_service.get_one(query, (session_id,))
        return Session(**row) if row else None

    def delete_session(self, session_id: str):
        query = "DELETE FROM session WHERE session_id = ?"
        self.db_service.execute(query, (session_id,))