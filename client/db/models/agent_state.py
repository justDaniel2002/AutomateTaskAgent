from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class AgentStatus(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing"
    WAITING = "waiting"
    ERROR = "error"


class AgentState(BaseModel):
    state_id: str
    session_id: str

    status: AgentStatus = AgentStatus.IDLE

    memory: dict = Field(default_factory=dict)
    context: dict = Field(default_factory=dict)

    current_task_id: Optional[str] = None
    updated_at: Optional[datetime] = None