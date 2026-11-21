from client.db.models.message import Message
from client.db.models.session import Session
from client.db.services.session_repository import SessionRepository
from client.pipeline.schemas import SimpleMessage

from .llm_client import get_model_response
from ..db.services.message_repository import MessageRepository
from ..db.services.db_service import DatabaseService
import uuid

MAX_TOOL_CALL_STEPS = 5

database_service = DatabaseService()  # This should be initialized with your actual database service
message_repo = MessageRepository(db=database_service)
session_repo = SessionRepository(db=database_service)  # Assuming you have a SessionRepository for session management

def save_message(message:str, session_id:str, role:str):
    message_repo.create(
        message=Message(
            message_id=str(uuid.uuid4()),
            session_id=session_id,
            role=role,
            content=message,
            metadata="{}",
        )
    )

def get_messages_by_session(session_id:str):
    return message_repo.get_by_session_id(session_id=session_id)

def ask_ai():
    while True:

        #fake data
        session_id = "session_123"
        #user input question
        print("___Automate Task Agent___")

        #get session 
        session = session_repo.get_by_id(session_id=session_id)
        if not session:
            print("Session not found. Creating a new session.")
            session_repo.create(Session(session_id=session_id, title="ThanhNC", status="active"))
            session = session_repo.get_by_id(session_id=session_id)

        messages = []
        messages_from_session = get_messages_by_session(session_id=session_id)
        if messages_from_session:
            print("Previous messages in this session:")
            for msg in messages_from_session:
                print(f"{msg.role}: {msg.content}")
            messages = messages_from_session

        question = input("Enter your question: ").strip()

        #call model to get response
        message = SimpleMessage(role="user", content=question)
        save_message(message.content, session_id, message.role)
        response = get_model_response(messages=messages + [message], config="You are a helpful assistant.")

        print("AI Response:", response.choices[0].message.content)
