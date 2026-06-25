# 01-NORTH_STAR.md: Intenção e Limites do Projeto
🎯 1. Intenção Central (The North Star)
R: Garantir que profissionais de saúde das UBS tenham acesso rápido e confiável à informação sobre disponibilidade de medicamentos, e que o responsável pela farmácia consiga atualizar os status em tempo real.

# 😫 2. O Problema Real (A Dor)
R: Nas Unidades Básicas de Saúde (UBS), a gestão de medicamentos é feita manualmente (planilhas ou papéis). Isso gera:

Informações desatualizadas sobre estoque

Dificuldade para saber se um medicamento está disponível, em falta ou a caminho

Falta de transparência para os profissionais que atendem os pacientes

Retrabalho e atraso no atendimento

# 👥 3. Público-Alvo (As Personas)
Persona	Descrição
Ana Clara Lima (Responsável pela Farmácia)	Profissional que gerencia o estoque. Precisa cadastrar medicamentos e atualizar status rapidamente.
Consultor (Enfermeira da UBS)	Precisa consultar se o medicamento prescrito está disponível antes de atender o paciente.
Dr. Ricardo (Médico da UBS)	Quer saber se o medicamento que vai prescrever tem estoque disponível.
João (Gestor Municipal de Saúde)	Precisa de visibilidade geral sobre a situação dos medicamentos em cada UBS do município.

# 🔍 4. Checklist de Descoberta (5 Questões)
Critério	Resposta
Fonte do Dado	Banco de dados local (SQLite) com lista de medicamentos pré-carregada do arquivo de classificação
Entrega	Interface web acessível via navegador na rede da UBS
Regra de Ouro	Apenas 1 responsável por município pode ALTERAR e CADASTRAR; demais só CONSULTAM
Resiliência	Sistema 100% offline (funciona apenas na rede local da UBS)
Interface	Limpa, simples, focada em consulta rápida e fácil para profissionais de saúde

# 🚫 5. Limites e Fora de Escopo
Para evitar o "scope creep" e manter a simplicidade Karpathy-style:

Não faremos	Motivo
❌ Login por redes sociais	Sistema local, não precisa
❌ Aplicativos mobile nativos	Web já atende
❌ Integração com sistemas externos (SUS, etc.)	MVP simples
❌ Reconhecimento facial ou biometria	Desnecessário
❌ Chatbot ou IA para atendimento	Fora do escopo
❌ Controle de validade de medicamentos	Futuro (desejável)
❌ Notificações push	MVP não precisa

# ⚖️ 6. Mindset de Simplicidade (Karpathy Style)
Regra 80/20: 80% do valor operacional será entregue com 20% do código.

Foco do MVP:

Página de login simples (responsável + consultores)

Página de consulta de medicamentos (lista + busca + status)

Página de gestão (para o responsável) com botões de edição de status

Páginas de guias (Insulina, Tabagismo, etc.) como conteúdo estático

4 status apenas: Disponível / Indisponível / Estoque baixo / Aguardando entrega

# 🛂 Instrução para a IA
"Antes de iniciar qualquer código, leia este NORTH_STAR. Qualquer funcionalidade sugerida que fira os limites do Item 5 ou o Mindset do Item 6 deve ser descartada imediatamente. Mantenha o foco no problema real: consulta e atualização de status de medicamentos por profissionais de saúde."

# ✅ Arquivo 01-NORTH_STAR.md criado com as informações DO SEU PROJETO (Farmácia Municipal de Itamonte).

Quer que eu continue gerando os outros arquivos da estrutura VEM para o seu projeto?

02-DERS_MESTRE.md

03-FRONTEND_GUIDE.md

04-BACKEND_GUIDE.md

SCHEMA.md

