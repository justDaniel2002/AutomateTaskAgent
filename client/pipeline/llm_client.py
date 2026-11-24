import os
from dotenv import load_dotenv
from openai import OpenAI
from .schemas import SimpleMessage
from ..helpers.data_loader import rules
from client.helpers.tools import tools
from openai import RateLimitError, APIStatusError

# Tải biến môi trường từ file .env
load_dotenv()

# Khởi tạo client trỏ về OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("MODEL", "particle-ai/particle-1:free")
MODEL_RETRY_ATTEMPTS = 3


def get_model_response(messages: list[SimpleMessage], config: str):
    common_rules = "".join(rules["commons"])

    send_messages = [{"role": "system", "content": f"{common_rules}\n{config}"}]
    for msg in messages:
        send_message = {"role": msg.role, "content": msg.content}
        if msg.tool_calls:
            send_message["tool_calls"] = msg.tool_calls
        if msg.tool_call_id:
            send_message["tool_call_id"] = msg.tool_call_id
        send_messages.append(send_message)
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=send_messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=500,
        )
    except RateLimitError as e:
        print("Rate limit error:", e)
        print("Response:", e.response.text)
        raise

    except APIStatusError as e:
        print("API status:", e.status_code)
        print("Response:", e.response.text)
        raise
    return response
