import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def classificar_intencao(pergunta):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt_sistema = """
Você é o analisador de intenções de um totem interativo de uma loja de roupas.
Responda APENAS com um JSON válido, sem formatação markdown (sem blocos ```json), no seguinte formato:
{
  "intencao": "NOVA_BUSCA" ou "SOBRE_PRODUTO" ou "OUTROS",
  "palavras_chave": ["produto", "marca", "cor"] // Lista de palavras-chave. Preencher APENAS se for NOVA_BUSCA.
}

Regras:
- NOVA_BUSCA: O usuário quer procurar um produto novo (ex: "tem leite?", "quero uma camisa nike").
- SOBRE_PRODUTO: O usuário quer detalhes do produto atual do contexto (ex: "onde fica isso?", "qual o preço?", "tem azul?").
- OUTROS: Saudações, despedidas ou perguntas totalmente aleatórias.
"""

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.0,
        "max_tokens": 100,
        "response_format": {"type": "json_object"}
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        # Limpar crases caso o LLM ainda as envie, mesmo com o aviso
        content = content.replace('```json', '').replace('```', '').strip()
        return json.loads(content)
    except Exception as e:
        print("Erro no classificar_intencao:", e)
        return {"intencao": "OUTROS", "palavras_chave": []}


def perguntar_llm(pergunta, contexto_produtos=None):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    if contexto_produtos:
        info_produtos = f"Produtos no contexto:\n{contexto_produtos}"
    else:
        info_produtos = "Nenhum produto no contexto atual."

    prompt_sistema = f"""
Você é o assistente virtual de um totem de uma loja de roupas.

Regras:
- Responda em frases curtas e diretas.
- Máximo 3 linhas.
- Fale preços no formato R$ 00,00.
- Linguagem natural, simpática e clara (ideal para resposta por voz).
- IMPORTANTE: Se o usuário perguntar algo totalmente aleatório fora do contexto de compras de roupas (ex: "quem descobriu o Brasil?", "piadas"), você DEVE educadamente desviar o assunto de volta para os produtos da loja de roupas.
- NUNCA use emojis ou asteriscos na resposta. O texto será lido por um sistema de voz.

{info_produtos}
"""

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": pergunta}
        ],
        "temperature": 0.2,
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Erro no perguntar_llm:", e)
        return "Desculpe, estou com problemas técnicos no momento."