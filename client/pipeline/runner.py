from client.db.models.session import Session
from client.db.services.db_service import DatabaseService
from client.db.services.message_repository import MessageRepository
from client.db.services.session_repository import SessionRepository
from client.db.services.task_repository import TaskRepository
from client.pipeline.steps import ask_ai


database_service = (
    DatabaseService()
)  
message_repo = MessageRepository(db=database_service)
session_repo = SessionRepository(db=database_service) 
task_repo = TaskRepository(db=database_service)


def get_messages_by_session(session_id: str):
    return message_repo.get_by_session_id(session_id=session_id)

def delete_messages_by_session(session_id: str):
    message_repo.delete_by_session_id(session_id=session_id)

def get_tasks_by_session(session_id:str):
    tasks = task_repo.get_by_session_id(session_id)
    if len(tasks) == 0:
        print("there is no task")
    else:
        for task in tasks:
            print("Tasl: ", task.description)

def runner():

    # fake data
    session_id = "session_123"
    # user input question
    print("___Automate Task Agent___")

    while True:
        # get session
        session = session_repo.get_by_id(session_id=session_id)
        if not session:
            print("Session not found. Creating a new session.")
            session_repo.create(
                Session(session_id=session_id, title="ThanhNC", status="active")
            )
            session = session_repo.get_by_id(session_id=session_id)

        messages = []
        messages_from_session = get_messages_by_session(session_id=session_id)
        # if messages_from_session:
        #     print("Previous messages in this session:")
        #     for msg in messages_from_session:
        #         print(f"{msg.role}: {msg.content}")
        #     messages = messages_from_session

        question = input("Enter your question: ").strip()

        if question.startswith("-del"):
            print("Deleting all messages in this session...")
            delete_messages_by_session(session_id=session_id)
            print("Messages deleted.")
            continue

        if question.startswith("-t"):
            get_tasks_by_session(session_id=session_id)
            continue

        if question.lower() == "exit":
            print("Exiting the agent.")
            break
        ask_ai(session_id=session_id, question=question, messages=messages)

