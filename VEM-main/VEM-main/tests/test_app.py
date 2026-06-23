import os
import unittest
import sqlite3
import json
from werkzeug.security import generate_password_hash

# Import Flask app
import app as my_app

class TestFarmaciaApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Override the database path for tests
        cls.test_db_path = os.path.join(my_app.BASE_DIR, "test_database.db")
        my_app.DB_PATH = cls.test_db_path

    def setUp(self):
        # 1. Arrange: Initialize a fresh test database with schema
        self.conn = sqlite3.connect(self.test_db_path)
        self.cursor = self.conn.cursor()
        
        # Create tables
        self.cursor.execute("DROP TABLE IF EXISTS logs_movimentacao;")
        self.cursor.execute("DROP TABLE IF EXISTS medicamentos;")
        self.cursor.execute("DROP TABLE IF EXISTS medicamentos_alto_custo;")
        self.cursor.execute("DROP TABLE IF EXISTS medicamentos_estrategicos;")
        self.cursor.execute("DROP TABLE IF EXISTS usuarios;")
        
        self.cursor.execute("""
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
        
        self.cursor.execute("""
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
        
        self.cursor.execute("""
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
        
        # Insert test users
        admin_hash = generate_password_hash("admin123")
        viewer_hash = generate_password_hash("consulta123")
        self.cursor.execute("INSERT INTO usuarios (username, password_hash, role, nome_completo, cidade) VALUES (?, ?, ?, ?, ?)",
                            ("responsavel", admin_hash, "admin", "Ana Clara Lima Barboza", "Itamonte"))
        self.cursor.execute("INSERT INTO usuarios (username, password_hash, role, nome_completo, cidade) VALUES (?, ?, ?, ?, ?)",
                            ("consultor", viewer_hash, "viewer", "Consultor Teste", "Itamonte"))
        
        # Insert test medications
        self.cursor.execute("INSERT INTO medicamentos (nome, classificacao, posologia, indicacao, status) VALUES (?, ?, ?, ?, ?)",
                            ("Dipirona 500mg cp", "ANALGÉSICOS E ANTIPIRÉTICOS", "1 cp a cada 6h", "Dor e febre", "Disponível"))
        self.cursor.execute("INSERT INTO medicamentos (nome, classificacao, posologia, indicacao, status) VALUES (?, ?, ?, ?, ?)",
                            ("Ibuprofeno 600mg", "ANTI-INFLAMATÓRIOS", "1 cp a cada 8h", "Inflamação", "Estoque baixo"))
        
        self.conn.commit()
        
        # Set up Flask test client
        my_app.app.config['TESTING'] = True
        my_app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = my_app.app.test_client()

    def tearDown(self):
        self.conn.close()
        # Clean up database file
        if os.path.exists(self.test_db_path):
            try:
                os.remove(self.test_db_path)
            except OSError:
                pass

    # --- TESTS ---

    def test_login_sucesso(self):
        """Test successful login returns redirect to dashboard"""
        # Arrange, Act
        response = self.client.post('/login', data={
            'username': 'responsavel',
            'password': 'admin123'
        }, follow_redirects=False)
        
        # Assert
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.location.endswith('/'))

    def test_login_senha_incorreta(self):
        """Test login with incorrect password returns error message"""
        # Arrange, Act
        response = self.client.post('/login', data={
            'username': 'responsavel',
            'password': 'wrongpassword'
        })
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Usu\xc3\xa1rio ou senha incorretos", response.data)

    def test_alterar_status_com_admin(self):
        """Test admin can successfully update medication status (expected 200)"""
        # Arrange
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'responsavel'
            sess['role'] = 'admin'
            sess['nome_completo'] = 'Ana Clara Lima Barboza'
            sess['cidade'] = 'Itamonte'
            
        # Act
        response = self.client.post('/api/alterar_status', 
                                    data=json.dumps({'medicamento_id': 1, 'novo_status': 'Indisponível'}),
                                    content_type='application/json')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data']['status_novo'], 'Indisponível')
        
        # Check in DB
        self.cursor.execute("SELECT status FROM medicamentos WHERE id = 1")
        status = self.cursor.fetchone()[0]
        self.assertEqual(status, 'Indisponível')

    def test_alterar_status_com_viewer(self):
        """Test viewer cannot update medication status (expected 401)"""
        # Arrange
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['username'] = 'consultor'
            sess['role'] = 'viewer'
            sess['nome_completo'] = 'Consultor Teste'
            sess['cidade'] = 'Itamonte'
            
        # Act
        response = self.client.post('/api/alterar_status', 
                                    data=json.dumps({'medicamento_id': 1, 'novo_status': 'Indisponível'}),
                                    content_type='application/json')
        
        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json['success'])
        self.assertEqual(response.json['error'], 'Unauthorized')

    def test_cadastrar_medicamento_com_admin(self):
        """Test admin can register a new medication (expected 200)"""
        # Arrange
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'responsavel'
            sess['role'] = 'admin'
            sess['nome_completo'] = 'Ana Clara Lima Barboza'
            sess['cidade'] = 'Itamonte'
            
        # Act
        response = self.client.post('/api/cadastrar_medicamento', 
                                    data=json.dumps({
                                        'nome': 'Amoxicilina 500mg cap',
                                        'classificacao': 'ANTIBIÓTICOS',
                                        'posologia': '1 cap de 8h em 8h',
                                        'indicacao': 'Infecções bacterianas',
                                        'status': 'Disponível'
                                    }),
                                    content_type='application/json')
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['data']['nome'], 'Amoxicilina 500mg cap')
        
        # Check in DB
        self.cursor.execute("SELECT COUNT(*) FROM medicamentos WHERE nome = 'Amoxicilina 500mg cap'")
        count = self.cursor.fetchone()[0]
        self.assertEqual(count, 1)

    def test_cadastrar_medicamento_com_viewer(self):
        """Test viewer cannot register a new medication (expected 401)"""
        # Arrange
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['username'] = 'consultor'
            sess['role'] = 'viewer'
            sess['nome_completo'] = 'Consultor Teste'
            sess['cidade'] = 'Itamonte'
            
        # Act
        response = self.client.post('/api/cadastrar_medicamento', 
                                    data=json.dumps({
                                        'nome': 'Amoxicilina 500mg cap',
                                        'classificacao': 'ANTIBIÓTICOS',
                                        'status': 'Disponível'
                                    }),
                                    content_type='application/json')
        
        # Assert
        self.assertEqual(response.status_code, 401)
        self.assertFalse(response.json['success'])

if __name__ == '__main__':
    unittest.main()
