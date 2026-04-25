import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def perguntar_llm(pergunta, contexto_produtos):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt_sistema = f"""
Você é o assistente de um totem de supermercado.

Regras:
- Responda em frases curtas
- Máximo 3 linhas
- Fale preço no formato R$ 00,00
- Linguagem natural e clara
- Ideal para resposta por voz

Produtos:
{contexto_produtos}
"""

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.2,
        "max_tokens": 120
    }

    response = requests.post(url, headers=headers, json=payload, timeout=20)
    data = response.json()

    return data["choices"][0]["message"]["content"]