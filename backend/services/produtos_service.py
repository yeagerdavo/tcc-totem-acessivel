import sqlite3

def listar_produtos_db():

    conn = sqlite3.connect("../database/produtos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    conn.close()

    return {"produtos": produtos}


def buscar_produto_db(nome):

    conn = sqlite3.connect("../database/produtos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", ('%' + nome + '%',))
    produtos = cursor.fetchall()

    conn.close()

    return {"resultado": produtos}