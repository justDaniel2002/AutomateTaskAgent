from client.db.models.message import Message
from client.db.models.session import Session
from client.db.services.session_repository import SessionRepository
from client.pipeline.schemas import SimpleMessage
from client.helpers.tools import execute_tool
from typing import Optional

from .llm_client import get_model_response
from ..db.services.message_repository import MessageRepository
from ..db.services.db_service import DatabaseService
import uuid

MAX_TOOL_CALL_STEPS = 5

database_service = (
    DatabaseService()
)  # This should be initialized with your actual database service
message_repo = MessageRepository(db=database_service)
session_repo = SessionRepository(
    db=database_service
)  # Assuming you have a SessionRepository for session management


def save_message(message: str, session_id: str, role: str):
    message_repo.create(
        message=Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=message,
            metadata="{}",
        )
    )


def send_messages(question: str, messages: list[SimpleMessage], role:str, session_id: str, tool_call_id: Optional[str] = None):
    message = SimpleMessage(role=role, content=question)
    save_message(message.content, session_id, message.role)
    if tool_call_id:
        message.tool_call_id = tool_call_id
    messages.append(message)
    print("send messages:", messages)
    response = get_model_response(
        messages=messages, config="You are a helpful assistant."
    )
    if response.choices[0].message.tool_calls:
        bot_message = SimpleMessage(
                    role="assistant", tool_calls=response.choices[0].message.tool_calls)
    else:
        bot_message = SimpleMessage(
                            role="assistant", content=response.choices[0].message.content)
    messages.append(bot_message)

    return response


def ask_ai(session_id: str, question: str, messages: list[SimpleMessage]):

    # call model to get response
    response = send_messages(question=question, messages=messages, role="user", session_id=session_id)

    if response.choices[0].message.tool_calls:
        for step in range(1, MAX_TOOL_CALL_STEPS):
            tool_call = response.choices[0].message.tool_calls
            if tool_call:
                print("calling tool", tool_call[0])
                result = execute_tool(tool_call[0])
                print("tool result", result)
                response = send_messages(question=result, messages=messages, role="tool", session_id=session_id,tool_call_id=tool_call[0].id)

    if response.choices[0].message.content:
        bot_message = SimpleMessage(
            role="assistant", content=response.choices[0].message.content
        )
        save_message(bot_message.content, session_id, bot_message.role)

    print("AI Response:", response.choices[0].message.content)
