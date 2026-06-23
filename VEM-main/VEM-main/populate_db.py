import os
import sqlite3
import json
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash

# Define absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

def init_db():
    print(f"Initializing database at: {DB_PATH}")
    
    # 1. Connect to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 2. Drop tables if they exist to start fresh
    cursor.execute("DROP TABLE IF EXISTS logs_movimentacao;")
    cursor.execute("DROP TABLE IF EXISTS medicamentos;")
    cursor.execute("DROP TABLE IF EXISTS medicamentos_alto_custo;")
    cursor.execute("DROP TABLE IF EXISTS medicamentos_estrategicos;")
    cursor.execute("DROP TABLE IF EXISTS usuarios;")
    
    # 3. Create table: medicamentos
    cursor.execute("""
    CREATE TABLE medicamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        classificacao TEXT NOT NULL,
        posologia TEXT,
        indicacao TEXT,
        status TEXT NOT NULL CHECK(status IN (
            'Disponível', 'Indisponível', 'Estoque baixo', 'Aguardando entrega', 'Farmácia Popular',
            'Disponível, Farmácia Popular', 'Estoque baixo, Farmácia Popular', 'Aguardando entrega, Farmácia Popular', 'Indisponível, Farmácia Popular'
        )),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 4. Create table: medicamentos_alto_custo
    cursor.execute("""
    CREATE TABLE medicamentos_alto_custo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        indicacao TEXT NOT NULL,
        cids TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 5. Create table: medicamentos_estrategicos
    cursor.execute("""
    CREATE TABLE medicamentos_estrategicos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        programa TEXT NOT NULL,
        posologia TEXT,
        indicacao TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 6. Create table: usuarios
    cursor.execute("""
    CREATE TABLE usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'viewer')),
        nome_completo TEXT,
        cidade TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 7. Create table: logs_movimentacao
    cursor.execute("""
    CREATE TABLE logs_movimentacao (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        medicamento_id INTEGER NOT NULL,
        medicamento_nome TEXT NOT NULL,
        status_anterior TEXT NOT NULL,
        status_novo TEXT NOT NULL,
        alterado_por TEXT NOT NULL,
        data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id) ON DELETE CASCADE
    );
    """)
    
    conn.commit()
    print("Database tables created successfully.")
    
   # 8. Insert Default Users
    # Admin (Ana Clara)
    admin_pw_hash = generate_password_hash("farmacia@2026!")
    cursor.execute("""
    INSERT INTO usuarios (username, password_hash, role, nome_completo, cidade)
    VALUES (?, ?, ?, ?, ?);
    """, ("Claralimabarboza", admin_pw_hash, "admin", "Ana Clara Lima Barboza", "Itamonte"))
    
    # Viewer (Consultor)
    viewer_pw_hash = generate_password_hash("consulta123")
    cursor.execute("""
    INSERT INTO usuarios (username, password_hash, role, nome_completo, cidade)
    VALUES (?, ?, ?, ?, ?);
    """, ("consultor", viewer_pw_hash, "viewer", "Consultor", "Itamonte"))
    
    conn.commit()
    print("Default users created:")
    print("  - admin: Claralimabarboza / farmacia@2026!")
    print("  - viewer: consultor / consulta123 (Nome: Consultor)")
    # 9. Load and insert standard medications
    meds_file = os.path.join(DATA_DIR, "medicamentos.json")
    if os.path.exists(meds_file):
        with open(meds_file, "r", encoding="utf-8") as f:
            meds = json.load(f)
        for m in meds:
            cursor.execute("""
            INSERT INTO medicamentos (nome, classificacao, posologia, indicacao, status)
            VALUES (?, ?, ?, ?, ?);
            """, (m["nome"], m["classificacao"], m["posologia"], m["indicacao"], m["status"]))
        conn.commit()
        print(f"Loaded {len(meds)} standard medications.")
    else:
        print(f"Warning: {meds_file} not found.")
        
    # 10. Load and insert CEAF high cost medications
    ac_file = os.path.join(DATA_DIR, "alto_custo.json")
    if os.path.exists(ac_file):
        with open(ac_file, "r", encoding="utf-8") as f:
            ac_meds = json.load(f)
        for m in ac_meds:
            cursor.execute("""
            INSERT INTO medicamentos_alto_custo (nome, indicacao, cids)
            VALUES (?, ?, ?);
            """, (m["nome"], m["indicacao"], m.get("cids", "")))
        conn.commit()
        print(f"Loaded {len(ac_meds)} high-cost medications.")
    else:
        print(f"Warning: {ac_file} not found.")
        
    # 11. Load and insert strategic medications
    est_file = os.path.join(DATA_DIR, "estrategicos.json")
    if os.path.exists(est_file):
        with open(est_file, "r", encoding="utf-8") as f:
            est_meds = json.load(f)
        for m in est_meds:
            cursor.execute("""
            INSERT INTO medicamentos_estrategicos (nome, programa, posologia, indicacao)
            VALUES (?, ?, ?, ?);
            """, (m["nome"], m["programa"], m.get("posologia", ""), m.get("indicacao", "")))
        conn.commit()
        print(f"Loaded {len(est_meds)} strategic medications.")
    else:
        print(f"Warning: {est_file} not found.")
        
    conn.close()
    print("Database population completed successfully!")

if __name__ == "__main__":
    init_db()
