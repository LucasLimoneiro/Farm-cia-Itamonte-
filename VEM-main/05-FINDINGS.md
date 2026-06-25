**Perfeito!** ✅

Agora vou criar o `05-FINDINGS.md` para o **SEU projeto** (Site Gestão de Medicamentos - Farmácia Municipal de Itamonte), seguindo **exatamente o mesmo formato, estrutura, emojis e estilo** do exemplo.

---

# 🧠 05-FINDINGS.md: Memória Técnica e Log de Autocura

## 🎯 1. Propósito e Uso

Este arquivo é o **Cérebro de Recuperação** do projeto **Site Gestão de Medicamentos - Farmácia Municipal de Itamonte**. Sempre que ocorrer um erro de execução, bug visual ou inconsistência de lógica, o erro deve ser colado aqui antes de solicitar a correção à IA.

**Protocolo de Autocura:**

1. Copie o erro/traceback do terminal ou console.
2. Cole na seção **"Log de Incidentes"** abaixo.
3. Invoque a IA com o comando: *"Analise os erros no FINDINGS.md, identifique a causa raiz e aplique uma correção cirúrgica no código"*.

---

## 📋 2. Log de Incidentes e Erros (The Log)

*Utilize esta tabela para registrar falhas técnicas e comportamentais da IA durante as sessões.*

| Data | Sessão (VCC) | Descrição do Erro / Traceback | Causa Raiz | Correção Cirúrgica Aplicada |
| :--- | :--- | :--- | :--- | :--- |
| [Data] | [ID-VCC] | [Cole o erro aqui] | [Ex: Falha ao carregar lista de medicamentos] | [Resumo da mudança] |
| [Data] | [ID-VCC] | [Ex: Botão de alterar status visível para consultor] | [Ex: Verificação de role na sessão] | [Adicionado `if session['role'] != 'admin': abort(401)`] |
| [Data] | [ID-VCC] | [Ex: Busca de medicamentos não filtra corretamente] | [Ex: Case sensitive no JavaScript] | [Adicionado `.toLowerCase()` na comparação] |

---

## 🔬 3. Análise de Causa Raiz (Root Cause) e Padrões

*Espaço para Maria (Revisora) ou Tiago (QA) documentarem por que erros recorrentes estão acontecendo.*

### Padrões Detectados no Projeto de Medicamentos:

| Padrão | Descrição | Ação Preventiva |
| :--- | :--- | :--- |
| **Status incorretos** | IA sugeriu status fora dos 4 permitidos (Disponível/Indisponível/Estoque baixo/Aguardando entrega) | Reforçar no `SCHEMA.md` e no `DERS_MESTRE.md` os 4 status fixos |
| **Caminhos relativos** | IA usou `./database.db` em vez de `os.path.abspath` | Reforçar regra no `04-BACKEND_GUIDE.md` |
| **Permissão de acesso** | IA permitiu que consultor visse botões de edição | Adicionar verificação `{% if session.role == 'admin' %}` nos templates |
| **CDN externa** | IA sugeriu Google Fonts ou Bootstrap CDN | Reforçar princípio Offline-First no `03-FRONTEND_GUIDE.md` |

---

## 💡 4. Decisões Técnicas e Trade-offs (Findings)

*Conforme as Karpathy Guidelines ("Think Before Coding"), registre aqui as premissas assumidas antes de grandes mudanças.*

| Decisão | Justificativa |
| :--- | :--- |
| **Uso de SQLite puro sem ORM** | Garantir latência zero, operação offline e seguir a regra de simplicidade 80/20 |
| **Design Glassmorphism adaptado para UBS** | Interface limpa, profissional e de fácil leitura para profissionais de saúde |
| **Apenas 1 responsável por município** | Simplifica a lógica de autorização e evita conflitos de edição simultânea |
| **4 status fixos** | Cobre todas as situações reais de uma farmácia de UBS sem complexidade desnecessária |
| **Pré-carga da lista de medicamentos (DOCX)** | Evita cadastro manual de centenas de itens e garante consistência dos dados |
| **Login simples (sem recuperação de senha)** | MVP voltado para uso interno da UBS; recuperação de senha pode ser adicionada depois |

---

## 📊 5. Métricas e Observações de Performance

*Registre aqui observações sobre desempenho do sistema em uso real.*

| Data | Observação | Status |
| :--- | :--- | :--- |
| [Data] | Carregamento da lista de 150+ medicamentos levou X segundos | ⏳ Pendente |
| [Data] | Busca em tempo real respondeu em menos de 100ms | ✅ Ok |
| [Data] | Alteração de status demorou X segundos para persistir | ⏳ Pendente |

---

## 🚧 6. Dívida Técnica e Lições Aprendidas

*O que ficou para o próximo giro do PDCA ou o que aprendemos que não deve ser repetido.*

### Lições Aprendidas:

1. **Lição:** Nunca importar fontes externas via CDN para manter o princípio **Offline-First** (ex: Google Fonts).
2. **Lição:** Sempre validar `session['role']` em TODAS as rotas sensíveis, não apenas no template.
3. **Lição:** A lista do DOCX tem centenas de itens; o `populate_db.py` deve ser testado antes da primeira execução.

### Dívida Técnica (para versões futuras):

| Item | Prioridade | Descrição |
| :--- | :--- | :--- |
| **Registro de movimentação (log)** | Média | Registrar data/hora e quem alterou cada status (desejável no DERS) |
| **Recuperação de senha** | Baixa | Para caso o responsável esqueça a senha de acesso |
| **Exportar lista de medicamentos** | Baixa | Gerar CSV/PDF da situação atual do estoque |
| **Múltiplas cidades** | Média | Expandir para outras UBS/municípios (multi-tenancy) |

---

## 🔄 7. Checklist de Autocura (Pré-commit)

*Antes de cada commit, a IA deve verificar se os seguintes pontos foram respeitados:*

- [ ] Nenhum caminho relativo para o banco de dados (`os.path.abspath` foi usado)
- [ ] Nenhuma CDN externa foi adicionada (tudo local ou sistema)
- [ ] Os 4 status estão sendo usados (nenhum status novo foi inventado)
- [ ] Apenas o responsável (admin) tem acesso a botões de edição/cadastro
- [ ] Logs detalhados foram adicionados para cada ação importante
- [ ] O sistema funciona completamente offline (testado sem internet)

---

## 📎 8. Apêndice: Comandos Úteis para Debug

```bash
# Recriar o banco de dados do zero
rm database.db && python populate_db.py

# Verificar estrutura das tabelas
sqlite3 database.db ".schema"

# Listar todos os medicamentos
sqlite3 database.db "SELECT nome, status FROM medicamentos;"

# Executar o servidor Flask em modo debug
python app.py --debug

# Testar rota de API diretamente
curl -X POST http://localhost:5000/api/alterar_status -H "Content-Type: application/json" -d '{"medicamento_id":1,"novo_status":"Indisponível"}'
```

---

### 🛂 Instrução para a IA

> *"Antes de cada correção, consulte as seções 2, 3 e 4 deste arquivo para garantir que a nova solução não repita erros do passado e mantenha as decisões arquiteturais já validadas. Ao encontrar um novo erro, registre-o imediatamente na seção 2 antes de corrigir"*.

---

✅ **Arquivo `05-FINDINGS.md` criado com as informações do SEU PROJETO!**

Quer que eu continue com o próximo arquivo (`SCHEMA.md` ou `06-WIREFRAME_IDEAS.md`)? Ou você vai me enviar outro arquivo para substituir? 🚀