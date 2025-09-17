import sqlite3
import csv
import os

DB_PATH = DB_PATH = r"C:\Users\willi\Desktop\meu_site\ubs_sp.db"
CSV_PATH = 'ubs_sp.csv'
CHUNK_SIZE = 500


def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS ubs (
    ID INTEGER PRIMARY KEY,
    LONG REAL,
    LAT REAL,
    SETCENS TEXT,
    AREAP REAL,
    CODDIST TEXT,
    DISTRITO TEXT,
    CODSUBPREF TEXT,
    SUBPREF TEXT,
    REGIAO5 TEXT
)
''')
conn.commit()


cursor.execute('DELETE FROM ubs')
conn.commit()
print("Tabela 'ubs' limpa. Inserindo novos dados...")

if not os.path.isfile(CSV_PATH):
    print(f"Arquivo CSV não encontrado: {CSV_PATH}")
    exit()

with open(CSV_PATH, newline='', encoding='latin-1') as csvfile:

    reader = csv.DictReader(csvfile)
    buffer = []
    rows_inserted = 0

    for row in reader:
        data = (
            to_int(row.get('ID')),
            to_float(row.get('LONG')),
            to_float(row.get('LAT')),
            row.get('SETCENS', '').strip(),
            to_float(row.get('AREAP')),
            row.get('CODDIST', '').strip(),
            row.get('DISTRITO', '').strip(),
            row.get('CODSUBPREF', '').strip(),
            row.get('SUBPREF', '').strip(),
            row.get('REGIAO5', '').strip()
        )
        buffer.append(data)


        if len(buffer) >= CHUNK_SIZE:
            cursor.executemany('''
                INSERT INTO ubs (ID, LONG, LAT, SETCENS, AREAP, CODDIST, DISTRITO, CODSUBPREF, SUBPREF, REGIAO5)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', buffer)
            conn.commit()
            rows_inserted += len(buffer)
            buffer = []


    if buffer:
        cursor.executemany('''
            INSERT INTO ubs (ID, LONG, LAT, SETCENS, AREAP, CODDIST, DISTRITO, CODSUBPREF, SUBPREF, REGIAO5)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', buffer)
        conn.commit()
        rows_inserted += len(buffer)

print(f"{rows_inserted} linhas inseridas com sucesso na tabela 'ubs'.")
conn.close()
