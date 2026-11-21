import os
from dotenv import load_dotenv
from openai import OpenAI
from .schemas import SimpleMessage
from ..helpers.data_loader import rules


# Tải biến môi trường từ file .env
load_dotenv()

# Khởi tạo client trỏ về OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = os.getenv("MODEL", "particle-ai/particle-1:free")
MODEL_RETRY_ATTEMPTS = 3

def get_model_response(messages:list[SimpleMessage], config:str):
    common_rules = "".join(rules["commons"])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": f"{common_rules}\n{config}"}] + 
        [{"role": msg.role, "content": msg.content} for msg in messages],
        max_tokens=500,
    )
    return response

