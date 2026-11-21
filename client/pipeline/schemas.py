from typing import Literal
from pydantic import BaseModel, Field

class SimpleMessage(BaseModel):
    role: str
    content: str = Field(min_length=1, max_length=20000)
