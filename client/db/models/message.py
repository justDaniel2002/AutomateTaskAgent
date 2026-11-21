from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Message(BaseModel):
    message_id: str
    session_id: str
    role: MessageRole = MessageRole.USER
    content: str
    metadata: str
    created_at: Optional[datetime] = None