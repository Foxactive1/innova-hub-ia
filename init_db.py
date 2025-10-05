### 🧱 init_db.py — Criação do Banco de Dados


import sqlite3

conn = sqlite3.connect('innova.db')
c = conn.cursor()

# Tabela de chaves (para futuras expansões)
c.execute('''CREATE TABLE IF NOT EXISTS keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    provider TEXT,
    name TEXT,
    key TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)''')

# Tabela de histórico de conversas
c.execute('''CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT,
    user_message TEXT,
    assistant_message TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)''')

conn.commit()
conn.close()
print('Banco de dados inicializado com sucesso!')