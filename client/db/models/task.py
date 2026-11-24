from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Task(BaseModel):
    task_id: str
    session_id: str
    name: str
    description: Optional[str] = None

    status: TaskStatus = TaskStatus.PENDING

    input_data: Optional[str] = None
    result: Optional[str] = None
    error: Optional[str] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None