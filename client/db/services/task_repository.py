
from typing import Optional

from client.db.models.task import Task
from client.db.services.db_service import DatabaseService


class TaskRepository:
    def __init__(self, db: DatabaseService):
        self.db = db

    def create(self, task: Task):
        query = "INSERT INTO task (task_id, session_id, name, description, status) VALUES (:task_id, :session_id, :name, :description, :status)"
        self.db.execute(query, task.model_dump())

    def update_status(self, task_id: str, status: str):
        query = "UPDATE task SET status = ? WHERE task_id = ?"
        self.db.execute(query, (status, task_id))

    def get_by_session_id(self, session_id: str) -> list[Optional[Task]]:
        query = "SELECT * FROM task WHERE session_id = ?"
        rows = self.db.get_all(query, (session_id,))
        return [Task(**dict(row)) for row in rows]

    def get_by_id(self, task_id: str) -> Optional[Task]:
        query = "SELECT * FROM task WHERE task_id = ?"
        row = self.db.get_one(query, (task_id,))
        if row:
            return Task(**dict(row))
        return None