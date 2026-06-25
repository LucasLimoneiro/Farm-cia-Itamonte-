📝 02-DERS_MESTRE.md: Especificação Mestre de Requisitos
📑 1. Identificação e Controle de Versão
Projeto: Site Gestão de Medicamentos - Farmácia Municipal de Itamonte.

Versão: 1.0 (Baseada no VEM).

Responsáveis: Equipe de Engenharia.

Histórico: Consolidação inicial pós-North Star.

# 🎯 2. Visão Geral e Escopo
Objetivo Central: Garantir que profissionais de saúde tenham acesso rápido à informação sobre disponibilidade de medicamentos, e que o responsável pela farmácia consiga atualizar os status em tempo real.

Público-Alvo: Ana Clara Lima (Responsável que precisa alterar/cadastrar) e Consultores (Profissionais que só consultam).

Fora de Escopo: Aplicativos nativos, login social, biometria e integração com sistemas externos (Princípio Karpathy contra o bloat).

# 👥 3. Requisitos de Usuário (RU)
Descrições abstratas das necessidades, escritas em linguagem natural para stakeholders.

RU01: O profissional de saúde deseja consultar rapidamente se um medicamento está disponível na farmácia antes de prescrever ou atender o paciente.

RU02: O responsável pela farmácia deseja atualizar o status de um medicamento (Disponível/Indisponível/Estoque baixo/Aguardando entrega) de forma simples e rápida.

RU03: O responsável pela farmácia deseja cadastrar novos medicamentos que não estão na lista padrão.

RU04: O gestor municipal deseja ter visibilidade geral sobre a situação dos medicamentos da sua cidade.

RU05: Qualquer profissional deseja acessar guias práticos (Insulina, Tabagismo, etc.) para consulta rápida.

# ⚙️ 4. Requisitos de Sistema (RS)
Detalhamento técnico das funções para orientar a implementação pela IA.

RS01: O sistema deve validar se o usuário tem permissão de responsável (acesso total) ou consultor (apenas leitura).

RS02: O motor de persistência deve utilizar SQLite local para garantir operação sem internet.

RS03: O sistema deve pré-carregar a lista de medicamentos a partir do arquivo medicamentos_classificacao.docx (centenas de registros com nome, classificação, posologia).

RS04: Os status possíveis para cada medicamento são fixos: Disponível, Indisponível, Estoque baixo, Aguardando entrega.

# ✅ 5. Requisitos Funcionais (RF) e Priorização
Funcionalidades específicas mapeadas por prioridade.

ID	Descrição do Requisito	Tipo	Prioridade	Critério de Aceite (Sucesso)
RF01	Exibir lista completa de medicamentos com status, classificação e posologia.	RS	Essencial	Profissional visualiza todos os medicamentos em < 3 segundos.
RF02	Permitir busca por nome do medicamento.	RS	Essencial	Busca retorna resultados em tempo real (filtro).
RF03	Permitir que o responsável altere o status de qualquer medicamento.	RS	Essencial	Status atualizado reflete imediatamente na lista.
RF04	Permitir que o responsável cadastre novos medicamentos.	RS	Importante	Novo medicamento aparece na lista após cadastro.
RF05	Login simples (usuário/senha) para diferenciar responsável de consultor.	RS	Essencial	Responsável tem botões de edição; consultor não.
RF06	Página separada com Guia Prático de Insulina (16 passos + NPH/Regular + agulhas + armazenamento).	RS	Importante	Conteúdo fiel aos anexos 3 e 4.
RF07	Página separada com Medicamentos de Alto Custo (CEAF) com lista, CIDs e indicações.	RS	Importante	Conteúdo fiel ao anexo 6.
RF08	Página separada com Medicamentos Estratégicos (Tuberculose, Hanseníase, Influenza, Chagas, Parasitoses).	RS	Importante	Conteúdo fiel aos anexos 7 e 8.
RF09	Página separada com Programa de Cessação do Tabagismo (Adesivos 7/14/21mg, Goma 2/4mg, Bupropiona).	RS	Importante	Conteúdo fiel aos anexos 9 e 10.
RF10	Página separada com Monitor de Glicose (como conseguir, tiras, quantidades).	RS	Desejável	Conteúdo fiel ao anexo 5.
Legenda de Prioridade:

Essencial: Imprescindível para o funcionamento básico (Regra 80/20).

Importante: O sistema opera sem ele, mas com lacunas de informação.

Desejável: Funcionalidades acessórias para versões futuras (Giro do PDCA).

# 📏 6. Regras de Negócio (RN)
Restrições que controlam a operação e a integridade do sistema.

ID	Descrição da Regra	Requisito Relacionado
RN01	Apenas o responsável (1 por município) pode alterar status e cadastrar medicamentos.	RF03, RF04, RF05
RN02	Demais profissionais (consultores) só podem visualizar medicamentos e guias.	RF01, RF02, RF05
RN03	Todo medicamento na lista DEVE ter um dos 4 status pré-definidos.	RS04
RN04	A lista inicial de medicamentos é pré-carregada do arquivo de classificação (não pode estar vazia).	RS03
RN05	As páginas de guias (Insulina, Tabagismo, etc.) são visíveis para TODOS os usuários (sem login obrigatório ou com login básico).	RF06, RF07, RF08, RF09, RF10
# 🛡️ 7. Requisitos Não Funcionais (RNF)
Atributos de qualidade seguindo o modelo FURPS.

ID	Nome / Atributo	Categoria	Prioridade	Descrição Técnica
RNF01	Latência Zero	Performance	Essencial	Carregamento da lista de medicamentos em < 2 segundos em rede local.
RNF02	Simplicidade de Uso	Usabilidade	Essencial	Interface limpa, sem treinamento prévio para profissionais de saúde.
RNF03	Offline-First	Confiabilidade	Essencial	Funcionar 100% sem dependência de internet externa.
RNF04	Acessibilidade	Usabilidade	Importante	Texto legível, contraste adequado para uso em UBS.
RNF05	Integridade de Dados	Confiabilidade	Essencial	Alterações de status devem ser persistidas no SQLite.
RNF06	Segurança Básica	Segurança	Essencial	Login simples mas que impeça acesso não autorizado às funções de edição.
# ⚖️ 8. Diretrizes Karpathy de Implementação (VEM)
Instruções comportamentais inegociáveis para a IA José e Ana.

Pense antes de codar: Explicite suposições no FINDINGS.md se o RF for ambíguo.

Simplicidade Radical: Implementar o código mínimo (Flask + SQLite + HTML/CSS Vanilla) para satisfazer o contrato.

Mudanças Cirúrgicas: Ao corrigir erros de validação, altere apenas as linhas afetadas no código.

Status Claros: Não inventar novos status; usar apenas os 4 definidos (Disponível/Indisponível/Estoque baixo/Aguardando entrega).

Conteúdo Fiel: Guias e listas de medicamentos devem seguir EXATAMENTE o conteúdo dos anexos fornecidos.

# 🔗 9. Matriz de Rastreabilidade Simples
Mapeamento para garantir que nenhum objetivo do North Star foi esquecido.

RU	Requisitos Relacionados
RU01 (Consultar medicamento)	RF01, RF02, RNF01, RNF02
RU02 (Atualizar status)	RF03, RN01, RNF05
RU03 (Cadastrar medicamento)	RF04, RN01
RU04 (Gestor visualizar geral)	RF01, RNF02
RU05 (Acessar guias)	RF06, RF07, RF08, RF09, RF10, RN05
💡 Instrução para a IA: Se durante o desenvolvimento for solicitada uma função que não esteja listada neste documento, você deve "empurrar de volta" (push back) citando a soberania do DERS e da Regra 80/20.

