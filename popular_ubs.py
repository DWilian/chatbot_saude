import sqlite3

DB_PATH_UBS = r"C:\Users\willi\Desktop\meu_site\ubs_sp.db"

conn = sqlite3.connect(DB_PATH_UBS)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ubs (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NOME TEXT NOT NULL,
    ENDERECO TEXT NOT NULL,
    LAT REAL,
    LONG REAL
)
""")

cursor.execute("DELETE FROM ubs")

ubs_teste = [
    ('UBS Centro', 'Rua A, 123', -23.659, -46.713),
    ('UBS Bairro', 'Rua B, 456', -23.660, -46.715),
    ('UBS Jardim', 'Rua C, 789', -23.661, -46.710),
    ('UBS Nova Esperança', 'Av. D, 101', -23.662, -46.712),
    ('UBS Saúde Total', 'Rua E, 202', -23.663, -46.716)
]

cursor.executemany("INSERT INTO ubs (NOME, ENDERECO, LAT, LONG) VALUES (?, ?, ?, ?)", ubs_teste)

conn.commit()
conn.close()
print("Tabela UBS criada e populada com sucesso!")
