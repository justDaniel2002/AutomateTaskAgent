
import datetime

from client.db.services.db_service import DatabaseService
from client.db.services.task_repository import TaskRepository
from client.db.models.task import Task
import uuid


db = DatabaseService()
task_repo = TaskRepository(db=db)

def create_task(session_id: str, description: str):
    task = Task(
        task_id=str(uuid.uuid4()),
        session_id=session_id,
        name=description,
        description=description,
        status="pending",
    )
    task_repo.create(task)
    return task

def update_task_status(task_id: str, status: str):
    task_repo.update_status(task_id, status)
    task = task_repo.get_by_id(task_id)
    return task

tools = [
    {
        "type": "function",
        "function": {
            "name": "create_task",
            "description": "Create a new task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {
                        "type": "string",
                        "description": "ID of the session"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the task"
                    }
                },
                "required": ["session_id", "description"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task_status",
            "description": "Update the status of a task. Possible statuses: pending, running, completed, failed, cancelled.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "ID of the task"
                    },
                    "status": {
                        "type": "string",
                        "description": "New status for the task"
                    }
                },
                "required": ["task_id", "status"],
                "additionalProperties": False
            }
        }
    }
]

import json

tool_registry = {
    "create_task": create_task,
    "update_task_status": update_task_status
}

def execute_tool(tool_call):
    function_name = tool_call.function.name

    arguments = json.loads(
        tool_call.function.arguments
    )

    function = tool_registry.get(function_name)

    if function is None:
        return "Error: Tool not found"

    result = function(**arguments)

    return str(result)