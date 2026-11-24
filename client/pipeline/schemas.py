from typing import Literal
from pydantic import BaseModel, Field
from typing import Optional, Any


class SimpleMessage(BaseModel):
    role: str
    content: Optional[str] = ""
    tool_calls: Any = None
    tool_call_id: Optional[str] = None
