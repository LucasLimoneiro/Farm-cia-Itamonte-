**Perfeito!** ✅

Vou gerar o **`SCHEMA.md`** - a "Constituição dos Dados" do seu projeto, seguindo o princípio **"JSON is Law"** e espelhando tanto no banco de dados (Ana/Backend) quanto nos formulários (José/Frontend).

---

# 📐 SCHEMA.md: Constituição dos Dados

## 🎯 1. Propósito e Princípio Fundamental

Este documento define a **estrutura inegociável dos dados** do projeto **Site Gestão de Medicamentos - Farmácia Municipal de Itamonte**.

> ### 🔒 "JSON is Law"
>
> *"O JSON definido aqui é a Única Fonte da Verdade. Toda tabela no SQLite, todo formulário no frontend e toda API deve espelhar EXATAMENTE estas estruturas de campos, tipos e nomes."*

**Consequências:**
- ❌ Nenhum campo pode ser adicionado no frontend sem estar no SCHEMA
- ❌ Nenhum campo pode ter nome diferente no banco de dados
- ✅ Qualquer mudança deve ser primeiro atualizada neste documento

---

## 📊 2. Tabelas do Banco de Dados (SQLite)

### 2.1 Tabela: `medicamentos`

*Lista principal de medicamentos da farmácia (fonte: `medicamentos_classificacao.docx`)*

| Campo | Tipo SQLite | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | SIM | Auto-incremento | 1 |
| `nome` | TEXT NOT NULL | SIM | Nome do medicamento + apresentação | "Dipirona 500mg cp" |
| `classificacao` | TEXT NOT NULL | SIM | Classificação farmacológica | "Analgésicos e Antipiréticos" |
| `posologia` | TEXT | NÃO | Dosagem e frequência | "500-1000mg a cada 6-8h (máx. 4g/dia)" |
| `indicacao` | TEXT | NÃO | Para que serve | "Dor e febre" |
| `status` | TEXT NOT NULL | SIM | Um dos 4 status permitidos | "Disponível" |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Data de cadastro | "2026-06-10 14:30:00" |
| `updated_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Última atualização | "2026-06-10 15:45:00" |

**Status permitidos (ENUM via CHECK constraint):**
```sql
status TEXT CHECK(status IN ('Disponível', 'Indisponível', 'Estoque baixo', 'Aguardando entrega', 'Farmácia Popular'))
```

**JSON equivalente:**
```json
{
  "id": 1,
  "nome": "Dipirona 500mg cp",
  "classificacao": "Analgésicos e Antipiréticos",
  "posologia": "500-1000mg a cada 6-8h (máx. 4g/dia)",
  "indicacao": "Dor e febre",
  "status": "Disponível",
  "created_at": "2026-06-10T14:30:00",
  "updated_at": "2026-06-10T15:45:00"
}
```

---

### 2.2 Tabela: `medicamentos_alto_custo`

*Medicamentos do Componente Especializado CEAF (fonte: lista fornecida)*

| Campo | Tipo SQLite | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | SIM | Auto-incremento | 1 |
| `nome` | TEXT NOT NULL | SIM | Nome + apresentação | "Abatacepte 125mg/mL Injetável" |
| `indicacao` | TEXT NOT NULL | SIM | Condição/doença tratada | "Artrite Reumatoide (≥18 anos)" |
| `cids` | TEXT | NÃO | Códigos CID relacionados | "M05.0-M06.8" |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Data de cadastro | "2026-06-10T14:30:00" |

**JSON equivalente:**
```json
{
  "id": 1,
  "nome": "Abatacepte 125mg/mL Injetável (Seringa Preenchida)",
  "indicacao": "Artrite Reumatoide (≥18 anos)",
  "cids": "M05.0-M06.8",
  "created_at": "2026-06-10T14:30:00"
}
```

---

### 2.3 Tabela: `medicamentos_estrategicos`

*Medicamentos Estratégicos (Tuberculose, Hanseníase, Influenza, Chagas, Parasitoses)*

| Campo | Tipo SQLite | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | SIM | Auto-incremento | 1 |
| `nome` | TEXT NOT NULL | SIM | Nome + apresentação | "Rifampicina 300mg" |
| `programa` | TEXT NOT NULL | SIM | Programa de saúde | "Tuberculose" |
| `posologia` | TEXT | NÃO | Dosagem e frequência | "10mg/kg/dia (máx. 600mg/dia), em jejum" |
| `indicacao` | TEXT | NÃO | Para que serve | "Tratamento da tuberculose ativa" |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Data de cadastro | "2026-06-10T14:30:00" |

**JSON equivalente:**
```json
{
  "id": 1,
  "nome": "Rifampicina 300mg",
  "programa": "Tuberculose",
  "posologia": "10mg/kg/dia (máx. 600mg/dia), em jejum",
  "indicacao": "Tratamento da tuberculose ativa em associação com outros tuberculostáticos",
  "created_at": "2026-06-10T14:30:00"
}
```

---

### 2.4 Tabela: `usuarios`

*Controle de acesso (responsável vs consultores)*

| Campo | Tipo SQLite | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | SIM | Auto-incremento | 1 |
| `username` | TEXT UNIQUE NOT NULL | SIM | Nome de usuário | "responsavel" |
| `password_hash` | TEXT NOT NULL | SIM | Hash da senha (werkzeug) | "pbkdf2:sha256:..." |
| `role` | TEXT NOT NULL | SIM | 'admin' ou 'viewer' | "admin" |
| `nome_completo` | TEXT | NÃO | Nome do profissional | "Carlos Silva" |
| `cidade` | TEXT NOT NULL | SIM | Município | "Itamonte" |
| `created_at` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Data de criação | "2026-06-10T14:30:00" |

**Role permitidas (ENUM via CHECK constraint):**
```sql
role TEXT CHECK(role IN ('admin', 'viewer'))
```

**JSON equivalente:**
```json
{
  "id": 1,
  "username": "responsavel",
  "password_hash": "pbkdf2:sha256:260000$...",
  "role": "admin",
  "nome_completo": "Carlos Silva",
  "cidade": "Itamonte",
  "created_at": "2026-06-10T14:30:00"
}
```

---

### 2.5 Tabela: `logs_movimentacao` (Desejável / Futuro)

*Registro de alterações de status para auditoria*

| Campo | Tipo SQLite | Obrigatório | Descrição | Exemplo |
| :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER PRIMARY KEY | SIM | Auto-incremento | 1 |
| `medicamento_id` | INTEGER NOT NULL | SIM | FOREIGN KEY → medicamentos.id | 1 |
| `medicamento_nome` | TEXT NOT NULL | SIM | Nome na época da alteração | "Dipirona 500mg cp" |
| `status_anterior` | TEXT NOT NULL | SIM | Status antes da mudança | "Disponível" |
| `status_novo` | TEXT NOT NULL | SIM | Status depois da mudança | "Indisponível" |
| `alterado_por` | TEXT NOT NULL | SIM | Nome do responsável | "Carlos Silva" |
| `data_hora` | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | SIM | Quando ocorreu | "2026-06-10T15:45:00" |

**JSON equivalente:**
```json
{
  "id": 1,
  "medicamento_id": 1,
  "medicamento_nome": "Dipirona 500mg cp",
  "status_anterior": "Disponível",
  "status_novo": "Indisponível",
  "alterado_por": "Carlos Silva",
  "data_hora": "2026-06-10T15:45:00"
}
```

---

## 🔄 3. API Endpoints e Payloads

### 3.1 POST `/api/alterar_status`

**Request (JSON):**
```json
{
  "medicamento_id": 1,
  "novo_status": "Indisponível"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Status alterado com sucesso",
  "data": {
    "id": 1,
    "nome": "Dipirona 500mg cp",
    "status_anterior": "Disponível",
    "status_novo": "Indisponível"
  }
}
```

**Response (Error - Permissão):**
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Apenas o responsável pode alterar status"
}
```

---

### 3.2 POST `/api/cadastrar_medicamento`

**Request (JSON):**
```json
{
  "nome": "Novo Medicamento 100mg",
  "classificacao": "Nova Classe",
  "posologia": "100mg a cada 12h",
  "indicacao": "Tratamento de X",
  "status": "Disponível"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Medicamento cadastrado com sucesso",
  "data": {
    "id": 153,
    "nome": "Novo Medicamento 100mg",
    "status": "Disponível"
  }
}
```

---

### 3.3 GET `/api/medicamentos`

**Response (JSON):**
```json
{
  "success": true,
  "total": 152,
  "data": [
    {
      "id": 1,
      "nome": "Dipirona 500mg cp",
      "classificacao": "Analgésicos e Antipiréticos",
      "posologia": "500-1000mg a cada 6-8h (máx. 4g/dia)",
      "indicacao": "Dor e febre",
      "status": "Disponível"
    }
  ]
}
```

---

### 3.4 POST `/login`

**Request (Form Data):**
```
username: responsavel
password: admin123
```

**Response (Redirect ou JSON):**
```json
{
  "success": true,
  "role": "admin",
  "redirect": "/"
}
```

---

## 🎨 4. Frontend JavaScript Objects

Os objetos JavaScript no frontend devem espelhar exatamente as estruturas JSON acima.

**Exemplo (lista de medicamentos):**
```javascript
// CORRETO ✅
const medicamento = {
    id: 1,
    nome: "Dipirona 500mg cp",
    classificacao: "Analgésicos e Antipiréticos",
    posologia: "500-1000mg a cada 6-8h (máx. 4g/dia)",
    indicacao: "Dor e febre",
    status: "Disponível"
};

// ERRADO ❌
const medicamento = {
    medicamento_id: 1,  // campo nome diferente
    name: "Dipirona",   // campo abreviado
    dose: "500mg"       // campo não definido no SCHEMA
};
```

---

## 🚫 5. Campos Proibidos (Anti-Bloat)

Para manter a simplicidade **Karpathy-style**, os seguintes campos NÃO devem ser incluídos no MVP:

| Campo | Motivo |
| :--- | :--- |
| `telefone` | Não necessário para o MVP |
| `endereco` | Fora do escopo |
| `data_nascimento` | Não relevante para gestão de medicamentos |
| `foto` | Aumenta complexidade sem valor agregado |
| `lote` | Futuro (controle de validade) |
| `validade` | Futuro (controle de validade) |

---

## 📝 6. Script SQL de Criação das Tabelas

```sql
-- Tabela: medicamentos
CREATE TABLE IF NOT EXISTS medicamentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    classificacao TEXT NOT NULL,
    posologia TEXT,
    indicacao TEXT,
    status TEXT NOT NULL CHECK(status IN ('Disponível', 'Indisponível', 'Estoque baixo', 'Aguardando entrega', 'Farmácia Popular')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: medicamentos_alto_custo
CREATE TABLE IF NOT EXISTS medicamentos_alto_custo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    indicacao TEXT NOT NULL,
    cids TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: medicamentos_estrategicos
CREATE TABLE IF NOT EXISTS medicamentos_estrategicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    programa TEXT NOT NULL,
    posologia TEXT,
    indicacao TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'viewer')),
    nome_completo TEXT,
    cidade TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela: logs_movimentacao (futuro)
CREATE TABLE IF NOT EXISTS logs_movimentacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    medicamento_id INTEGER NOT NULL,
    medicamento_nome TEXT NOT NULL,
    status_anterior TEXT NOT NULL,
    status_novo TEXT NOT NULL,
    alterado_por TEXT NOT NULL,
    data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (medicamento_id) REFERENCES medicamentos(id)
);
```

---

### 🛂 Instrução para a IA

> *"José (Frontend) e Ana (Backend): antes de qualquer implementação, consultem este SCHEMA.md. Nenhum campo pode ser adicionado, renomeado ou removido sem primeiro atualizar este documento. O princípio é: JSON is Law."*

---

✅ **`SCHEMA.md` criado com todas as tabelas e estruturas do SEU PROJETO!**

---

## 🚀 Próximo passo

Quer que eu:

| Opção | Descrição |
| :--- | :--- |
| **2** | Gerar o arquivo `medicamentos_alto_custo.json` (pronto para importação) |
| **3** | Gerar o arquivo `medicamentos.json` (a partir do DOCX) |
| **4** | Continuar com o próximo arquivo da metodologia VEM (`07-VCC_TEMPLATE.md`) |
| **5** | Começar a gerar o código do sistema (app.py, templates, etc.) |

**Me diga!** 🚀