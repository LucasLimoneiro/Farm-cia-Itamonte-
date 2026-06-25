import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def migrate_db():
    print(f"Migrating database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Disable foreign keys temporarily
    cursor.execute("PRAGMA foreign_keys = OFF;")
    
    # 1. Rename old table
    cursor.execute("ALTER TABLE medicamentos RENAME TO medicamentos_old;")
    
    # 2. Create new table with expanded CHECK constraint
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
    
    # 3. Copy data from old table to new table
    cursor.execute("""
    INSERT INTO medicamentos (id, nome, classificacao, posologia, indicacao, status, created_at, updated_at)
    SELECT id, nome, classificacao, posologia, indicacao, status, created_at, updated_at
    FROM medicamentos_old;
    """)
    
    # 4. Drop the old table
    cursor.execute("DROP TABLE medicamentos_old;")
    
    # Re-enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    conn.commit()
    conn.close()
    print("Migration completed successfully!")

if __name__ == "__main__":
    migrate_db()
