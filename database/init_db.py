import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "produtos.db")

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    categoria TEXT,
    tipo TEXT,
    cor TEXT,
    tamanho TEXT,
    marca TEXT,
    preco REAL,
    estoque INTEGER,
    setor TEXT,
    corredor TEXT,
    prateleira TEXT,
    descricao TEXT
)
""")

produtos = [

# ROUPAS
("Camisa Dry Fit", "Roupa", "Treino", "Preta", "GG", "Nike", 79.90, 8, "Esportivo", "2", "Arara 4", "Camisa esportiva respirável"),
("Camisa Dry Fit", "Roupa", "Treino", "Azul", "GG", "Nike", 79.90, 6, "Esportivo", "2", "Arara 4", "Camisa esportiva respirável"),
("Bermuda Running", "Roupa", "Treino", "Preta", "G", "Adidas", 89.90, 5, "Esportivo", "2", "Arara 5", "Bermuda leve esportiva"),

# MERCEARIA
("Arroz 5kg", "Alimento", "Arroz", "Branco", "5kg", "Camil", 28.90, 15, "Mercearia", "3", "Prateleira 2", "Arroz tipo 1"),
("Feijão Carioca 1kg", "Alimento", "Feijão", "Bege", "1kg", "Kicaldo", 8.90, 22, "Mercearia", "3", "Prateleira 3", "Feijão carioca"),
("Café 500g", "Alimento", "Café", "N/A", "500g", "Pilão", 16.90, 19, "Mercearia", "4", "Prateleira 1", "Café torrado"),

# LIMPEZA
("Sabão em Pó 1kg", "Limpeza", "Sabão", "Azul", "1kg", "OMO", 12.90, 16, "Limpeza", "6", "Prateleira 2", "Sabão em pó"),

# BEBIDAS
("Água Mineral 500ml", "Bebida", "Água", "Transparente", "500ml", "Crystal", 3.50, 100, "Bebidas", "1", "Geladeira 1", "Água sem gás")
]

cursor.executemany("""
INSERT INTO produtos (
nome, categoria, tipo, cor, tamanho, marca,
preco, estoque, setor, corredor, prateleira, descricao
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("Banco profissional criado com sucesso.")