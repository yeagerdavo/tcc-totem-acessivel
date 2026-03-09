import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "produtos.db")

# Apaga o banco antigo para recriar do zero
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL,
    descricao TEXT,
    estoque INTEGER NOT NULL
)
""")

produtos = [
    ("Água Mineral 500ml", "Bebida", 3.50, "Garrafa de água mineral sem gás", 100),
    ("Água com Gás 500ml", "Bebida", 4.00, "Garrafa de água com gás", 80),
    ("Coca-Cola Lata 350ml", "Bebida", 6.00, "Refrigerante Coca-Cola lata", 50),
    ("Guaraná Lata 350ml", "Bebida", 5.50, "Refrigerante sabor guaraná", 45),
    ("Suco de Laranja 300ml", "Bebida", 7.00, "Suco pronto sabor laranja", 30),

    ("Chocolate ao Leite 90g", "Doce", 5.00, "Barra de chocolate ao leite", 40),
    ("Chocolate Amargo 80g", "Doce", 6.50, "Barra de chocolate amargo", 25),
    ("Bala de Goma 100g", "Doce", 4.50, "Pacote de bala de goma", 60),
    ("Paçoca", "Doce", 2.00, "Doce de amendoim tipo paçoca", 70),

    ("Salgadinho Queijo 80g", "Snack", 8.00, "Salgadinho sabor queijo", 35),
    ("Batata Chips 120g", "Snack", 9.50, "Batata frita crocante", 20),
    ("Amendoim Torrado 150g", "Snack", 7.50, "Pacote de amendoim torrado", 28),

    ("Arroz 5kg", "Mercearia", 28.90, "Pacote de arroz branco tipo 1", 15),
    ("Feijão Carioca 1kg", "Mercearia", 8.90, "Pacote de feijão carioca", 22),
    ("Macarrão Espaguete 500g", "Mercearia", 5.20, "Macarrão tipo espaguete", 33),
    ("Molho de Tomate 340g", "Mercearia", 3.80, "Molho de tomate tradicional", 40),
    ("Óleo de Soja 900ml", "Mercearia", 7.90, "Óleo de soja refinado", 18),
    ("Açúcar 1kg", "Mercearia", 4.80, "Açúcar refinado", 26),
    ("Café 500g", "Mercearia", 16.90, "Café torrado e moído", 19),

    ("Sabonete 90g", "Higiene", 2.50, "Sabonete corporal", 55),
    ("Shampoo 350ml", "Higiene", 14.90, "Shampoo para uso diário", 17),
    ("Creme Dental 90g", "Higiene", 6.90, "Pasta de dente com flúor", 29),
    ("Papel Higiênico 12 rolos", "Higiene", 18.50, "Pacote com 12 rolos", 14),

    ("Detergente 500ml", "Limpeza", 3.20, "Detergente líquido neutro", 38),
    ("Sabão em Pó 1kg", "Limpeza", 12.90, "Sabão em pó para roupas", 16),
    ("Água Sanitária 1L", "Limpeza", 4.70, "Água sanitária multiuso", 24)
]

cursor.executemany("""
INSERT INTO produtos (nome, categoria, preco, descricao, estoque)
VALUES (?, ?, ?, ?, ?)
""", produtos)

conn.commit()
conn.close()

print("Banco de dados recriado com sucesso")