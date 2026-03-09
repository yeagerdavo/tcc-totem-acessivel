from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "produtos.db")

def conectar_bd():
    return sqlite3.connect(DB_PATH)

def formatar_produto(produto):
    return {
        "id": produto[0],
        "nome": produto[1],
        "categoria": produto[2],
        "preco": produto[3],
        "descricao": produto[4],
        "estoque": produto[5]
    }

@app.get("/")
def home():
    return {"mensagem": "Totem funcionando"}

@app.get("/produtos")
def listar_produtos():
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()

    produtos_formatados = [formatar_produto(produto) for produto in produtos]

    return {"produtos": produtos_formatados}

@app.get("/buscar-produto")
def buscar_produto(nome: str):
    conn = conectar_bd()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
    produtos = cursor.fetchall()

    conn.close()

    produtos_formatados = [formatar_produto(produto) for produto in produtos]

    return {"resultado": produtos_formatados}