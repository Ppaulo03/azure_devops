import os
import httpx
from dotenv import load_dotenv

load_dotenv()

EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE")
TARGET_PHONE = os.getenv("TARGET_PHONE", "").replace("+", "").replace("-", "").replace(" ", "")

async def send_whatsapp_message(text: str):
    if not all([EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE, TARGET_PHONE]):
        print("Erro: Configurações da Evolution API incompletas no .env")
        return

    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "number": TARGET_PHONE,
        "text": text,
        "options": {
            "delay": 100,
            "presence": "composing",
            "linkPreview": False
        }
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(f"Mensagem enviada com sucesso: {text}")
    except Exception as e:
        print(f"Erro ao enviar mensagem via Evolution API: {e}")
