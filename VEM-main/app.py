import os
import sqlite3
import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "vem_itamonte_secret_key_extremely_secure"

# Absolute path for the SQLite database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Helper to execute queries
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Enforce login filter
@app.before_request
def require_login():
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'user_id' not in session:
        return redirect(url_for('login'))

# ROTA: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
        
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = query_db("SELECT * FROM usuarios WHERE username = ?", (username,), one=True)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['nome_completo'] = user['nome_completo']
            session['cidade'] = user['cidade']
            print(f"[LOGIN] Usuário [{username}] logado com role [{user['role']}] na cidade [{user['cidade']}].")
            return redirect(url_for('index'))
        else:
            error = "Usuário ou senha incorretos."
            print(f"[WARN] Tentativa de login malsucedida para o usuário [{username}].")
            
    return render_template('login.html', error=error)

# ROTA: Logout
@app.route('/logout')
def logout():
    username = session.get('username')
    session.clear()
    print(f"[LOGOUT] Usuário [{username}] deslogado.")
    return redirect(url_for('login'))

# ROTA: Dashboard (Página Inicial)
@app.route('/')
def index():
    return render_template('index.html')

# ROTA: Medicamentos (HTML View)
@app.route('/medicamentos')
def medicamentos_view():
    # Fetch initial list to render server-side (Jinja2)
    meds = query_db("SELECT * FROM medicamentos ORDER BY nome ASC")
    # Fetch unique classifications for the filter dropdown
    classifications = query_db("SELECT DISTINCT classificacao FROM medicamentos ORDER BY classificacao ASC")
    return render_template('medicamentos.html', medicamentos=meds, classifications=classifications)

# API: GET Medicamentos JSON
@app.route('/api/medicamentos')
def api_medicamentos():
    meds = query_db("SELECT * FROM medicamentos ORDER BY nome ASC")
    data = []
    for m in meds:
        data.append({
            "id": m["id"],
            "nome": m["nome"],
            "classificacao": m["classificacao"],
            "posologia": m["posologia"],
            "indicacao": m["indicacao"],
            "status": m["status"],
            "updated_at": m["updated_at"]
        })
    return jsonify({"success": True, "total": len(data), "data": data})

# API: POST Alterar Status (Admin Only)
@app.route('/api/alterar_status', methods=['POST'])
def api_alterar_status():
    if session.get('role') != 'admin' or session.get('nome_completo') != 'Ana Clara Lima Barboza':
        print(f"[UNAUTHORIZED] Tentativa não autorizada de alterar status por usuário [{session.get('username')}].")
        return jsonify({"success": False, "error": "Unauthorized", "message": "Apenas o responsável pode alterar status"}), 401
        
    data = request.get_json()
    if not data or 'medicamento_id' not in data or 'novo_status' not in data:
        return jsonify({"success": False, "error": "Bad Request", "message": "Parâmetros ausentes"}), 400
        
    med_id = data['medicamento_id']
    novo_status = data['novo_status']
    
    # Validate status values
    valid_statuses = [
        'Disponível', 'Indisponível', 'Estoque baixo', 'Aguardando entrega', 'Farmácia Popular',
        'Disponível, Farmácia Popular', 'Estoque baixo, Farmácia Popular', 'Aguardando entrega, Farmácia Popular', 'Indisponível, Farmácia Popular'
    ]
    if novo_status not in valid_statuses:
        return jsonify({"success": False, "error": "Bad Request", "message": "Status inválido"}), 400
        
    db = get_db()
    # Find current status for logging
    med = query_db("SELECT * FROM medicamentos WHERE id = ?", (med_id,), one=True)
    if not med:
        return jsonify({"success": False, "error": "Not Found", "message": "Medicamento não encontrado"}), 404
        
    status_anterior = med['status']
    nome_medicamento = med['nome']
    
    # Update status in db
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.execute("""
    UPDATE medicamentos 
    SET status = ?, updated_at = ? 
    WHERE id = ?;
    """, (novo_status, now, med_id))
    
    # Write log to logs_movimentacao
    db.execute("""
    INSERT INTO logs_movimentacao (medicamento_id, medicamento_nome, status_anterior, status_novo, alterado_por)
    VALUES (?, ?, ?, ?, ?);
    """, (med_id, nome_medicamento, status_anterior, novo_status, session.get('nome_completo')))
    
    db.commit()
    print(f"[SUCCESS] Status de [{nome_medicamento}] alterado de [{status_anterior}] para [{novo_status}] por [{session.get('username')}].")
    
    return jsonify({
        "success": True,
        "message": "Status alterado com sucesso",
        "data": {
            "id": med_id,
            "nome": nome_medicamento,
            "status_anterior": status_anterior,
            "status_novo": novo_status
        }
    })

# API: POST Cadastrar Medicamento (Admin Only)
@app.route('/api/cadastrar_medicamento', methods=['POST'])
def api_cadastrar_medicamento():
    if session.get('role') != 'admin' or session.get('nome_completo') != 'Ana Clara Lima Barboza':
        print(f"[UNAUTHORIZED] Tentativa não autorizada de cadastrar medicamento por usuário [{session.get('username')}].")
        return jsonify({"success": False, "error": "Unauthorized", "message": "Apenas o responsável pode cadastrar medicamentos"}), 401
        
    data = request.get_json()
    if not data or 'nome' not in data or 'classificacao' not in data or 'status' not in data:
        return jsonify({"success": False, "error": "Bad Request", "message": "Parâmetros obrigatórios ausentes"}), 400
        
    nome = data['nome'].strip()
    classificacao = data['classificacao'].strip()
    posologia = data.get('posologia', '').strip()
    indicacao = data.get('indicacao', '').strip()
    status = data['status']
    
    if not nome or not classificacao:
        return jsonify({"success": False, "error": "Bad Request", "message": "Nome e classificação não podem ser vazios"}), 400
        
    # Validate status values
    valid_statuses = [
        'Disponível', 'Indisponível', 'Estoque baixo', 'Aguardando entrega', 'Farmácia Popular',
        'Disponível, Farmácia Popular', 'Estoque baixo, Farmácia Popular', 'Aguardando entrega, Farmácia Popular', 'Indisponível, Farmácia Popular'
    ]
    if status not in valid_statuses:
        return jsonify({"success": False, "error": "Bad Request", "message": "Status inválido"}), 400
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    INSERT INTO medicamentos (nome, classificacao, posologia, indicacao, status)
    VALUES (?, ?, ?, ?, ?);
    """, (nome, classificacao, posologia, indicacao, status))
    new_id = cursor.lastrowid
    db.commit()
    
    print(f"[ADD] Novo medicamento [{nome}] cadastrado com ID [{new_id}] por [{session.get('username')}].")
    
    return jsonify({
        "success": True,
        "message": "Medicamento cadastrado com sucesso",
        "data": {
            "id": new_id,
            "nome": nome,
            "classificacao": classificacao,
            "status": status
        }
    })

# ROTA: Guia Prático de Insulina (HTML View)
@app.route('/guia-insulina')
def guia_insulina():
    return render_template('guia_insulina.html')

# ROTA: Medicamentos de Alto Custo (CEAF) (HTML View)
@app.route('/alto-custo')
def alto_custo():
    ac_meds = query_db("SELECT * FROM medicamentos_alto_custo ORDER BY nome ASC")
    return render_template('alto_custo.html', medicamentos=ac_meds)

# API: GET CEAF JSON
@app.route('/api/medicamentos_alto_custo')
def api_alto_custo():
    ac_meds = query_db("SELECT * FROM medicamentos_alto_custo ORDER BY nome ASC")
    data = []
    for m in ac_meds:
        data.append({
            "id": m["id"],
            "nome": m["nome"],
            "indicacao": m["indicacao"],
            "cids": m["cids"]
        })
    return jsonify({"success": True, "total": len(data), "data": data})

# ROTA: Medicamentos Estratégicos (HTML View)
@app.route('/estrategicos')
def estrategicos():
    est_meds = query_db("SELECT * FROM medicamentos_estrategicos ORDER BY programa ASC, nome ASC")
    return render_template('estrategicos.html', medicamentos=est_meds)

# API: GET Estratégicos JSON
@app.route('/api/medicamentos_estrategicos')
def api_estrategicos():
    est_meds = query_db("SELECT * FROM medicamentos_estrategicos ORDER BY nome ASC")
    data = []
    for m in est_meds:
        data.append({
            "id": m["id"],
            "nome": m["nome"],
            "programa": m["programa"],
            "posologia": m["posologia"],
            "indicacao": m["indicacao"]
        })
    return jsonify({"success": True, "total": len(data), "data": data})

# ROTA: Cessação do Tabagismo (HTML View)
@app.route('/tabagismo')
def tabagismo():
    return render_template('tabagismo.html')

# ROTA: Monitor de Glicose (HTML View)
@app.route('/monitor-glicose')
def monitor_glicose():
    return render_template('monitor_glicose.html')

# ROTA: Admin Dashboard (HTML View)
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin' or session.get('nome_completo') != 'Ana Clara Lima Barboza':
        return redirect(url_for('index'))
    
    db = get_db()
    # Resumo Geral
    meds = db.execute("SELECT status FROM medicamentos").fetchall()
    total = len(meds)
    disponiveis = sum(1 for m in meds if m['status'] == 'Disponível')
    atencao = sum(1 for m in meds if m['status'] in ['Estoque baixo', 'Indisponível', 'Aguardando entrega'])
    popular = sum(1 for m in meds if m['status'] == 'Farmácia Popular')
    
    # Resumo por Classe
    classes_query = db.execute("""
        SELECT classificacao as classe, 
               COUNT(*) as total,
               SUM(CASE WHEN status = 'Disponível' THEN 1 ELSE 0 END) as disponivel,
               SUM(CASE WHEN status = 'Estoque baixo' THEN 1 ELSE 0 END) as est_baixo,
               SUM(CASE WHEN status = 'Indisponível' THEN 1 ELSE 0 END) as indisponivel
        FROM medicamentos 
        GROUP BY classificacao
        ORDER BY total DESC
    """).fetchall()
    
    classifications = db.execute("SELECT DISTINCT classificacao FROM medicamentos ORDER BY classificacao ASC").fetchall()
    
    return render_template('admin_dashboard.html', 
                          total=total, 
                          disponiveis=disponiveis, 
                          atencao=atencao, 
                          popular=popular,
                          classes=classes_query,
                          classifications=classifications)

# ROTA: Admin Medicamentos (HTML View)
@app.route('/admin/medicamentos')
def admin_medicamentos():
    if session.get('role') != 'admin' or session.get('nome_completo') != 'Ana Clara Lima Barboza':
        return redirect(url_for('index'))
        
    db = get_db()
    meds = db.execute("SELECT * FROM medicamentos ORDER BY nome ASC").fetchall()
    classifications = db.execute("SELECT DISTINCT classificacao FROM medicamentos ORDER BY classificacao ASC").fetchall()
    
    return render_template('admin_medicamentos.html', medicamentos=meds, classifications=classifications)

if __name__ == "__main__":
    # In production/UBS, it will run locally on 0.0.0.0 to be accessible on the local network
    app.run(host="0.0.0.0", port=5000, debug=True)
