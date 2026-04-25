import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "..", "database", "produtos.db")

memoria = {
    "ultimo_produto": None,
    "aguardando_localizacao": False
}


def conectar_bd():
    return sqlite3.connect(DB_PATH)


def formatar_produto(produto):
    return {
        "id": produto[0],
        "nome": produto[1],
        "categoria": produto[2],
        "tipo": produto[3],
        "cor": produto[4],
        "tamanho": produto[5],
        "marca": produto[6],
        "preco": produto[7],
        "estoque": produto[8],
        "setor": produto[9],
        "corredor": produto[10],
        "prateleira": produto[11],
        "descricao": produto[12]
    }


def buscar_produtos(texto):
    texto = texto.lower()

    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()

    encontrados = []

    for p in produtos:
        item = formatar_produto(p)

        score = 0

        campos = [
            item["nome"],
            item["categoria"],
            item["tipo"],
            item["cor"],
            item["tamanho"],
            item["marca"]
        ]

        for campo in campos:
            if campo and campo.lower() in texto:
                score += 3

        for palavra in texto.split():
            for campo in campos:
                if campo and palavra in campo.lower():
                    score += 1

        if score > 0:
            item["score"] = score
            encontrados.append(item)

    encontrados.sort(key=lambda x: x["score"], reverse=True)

    return encontrados


def responder_localizacao():
    produto = memoria["ultimo_produto"]

    if not produto:
        return {
            "resposta": "Nenhum produto foi consultado.",
            "resultados": []
        }

    memoria["aguardando_localizacao"] = False

    resposta = (
        f"{produto['nome']} está no setor {produto['setor']}, "
        f"corredor {produto['corredor']}, "
        f"{produto['prateleira']}."
    )

    return {
        "resposta": resposta,
        "resultados": [produto]
    }


def pipeline_processar(pergunta):

    texto = pergunta.lower().strip()

    # resposta de contexto para localização
    if memoria["aguardando_localizacao"]:

        if (
            "sim" in texto or
            "claro" in texto or
            "quero" in texto or
            "pode" in texto or
            "onde" in texto or
            "aonde" in texto or
            "localização" in texto or
            "localizacao" in texto or
            "me fala" in texto or
            "me diga" in texto or
            "quero saber" in texto
        ):
            return responder_localizacao()

    # pergunta direta de localização
    if (
        "onde fica" in texto or
        "aonde fica" in texto or
        "onde está" in texto or
        "aonde está" in texto or
        "onde encontro" in texto
    ):
        return responder_localizacao()

    resultados = buscar_produtos(texto)

    if not resultados:
        return {
            "resposta": "Não encontrei esse produto, mas posso buscar algo parecido.",
            "resultados": []
        }

    principal = resultados[0]

    memoria["ultimo_produto"] = principal
    memoria["aguardando_localizacao"] = True

    resposta = (
        f"Temos {principal['nome']} "
        f"por R$ {principal['preco']:.2f}. "
        f"Deseja saber onde encontrar?"
    )

    return {
        "resposta": resposta,
        "resultados": resultados[:3]
    }