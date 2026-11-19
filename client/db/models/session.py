from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Session(BaseModel):
    session_id: str
    title: Optional[str] = None
    status: SessionStatus = SessionStatus.ACTIVE
    created_at: Optional[datetime] = None