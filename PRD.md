# PRD - Ebook Factory

## 1. Visão Geral

### Objetivo

Construir uma plataforma de geração de ebooks para publicação na Amazon KDP utilizando Inteligência Artificial e Human-In-The-Loop.

O sistema deve conduzir o usuário desde a ideação do livro até a geração de um arquivo compatível com a Amazon KDP.

O foco não é apenas gerar texto, mas fornecer um workflow estruturado, iterativo e auditável, permitindo que o usuário participe das decisões em todas as etapas críticas.

---

# 2. Objetivos do Produto

## Objetivos Principais

* Gerar ebooks completos utilizando IA.
* Permitir revisão humana em cada etapa.
* Aplicar Reflection Pattern para melhoria contínua dos resultados.
* Manter histórico e versionamento dos artefatos.
* Produzir arquivos compatíveis com Amazon KDP.
* Disponibilizar observabilidade completa dos workflows de IA.

## Não Objetivos (MVP)

* Publicação automática na Amazon KDP.
* Geração de audiobooks.
* Marketplace de ebooks.
* Colaboração multiusuário em tempo real.

---

# 3. Fluxo do Produto

## Etapa 1 - Ideação

### Objetivo

Transformar uma ideia inicial em uma proposta estruturada de livro.

### Entrada

* Nicho
* Tema
* Público-alvo (opcional)

### Saída

* Título
* Subtítulo
* Persona
* Problema principal
* Promessa do livro
* Sumário preliminar

### Workflow

Idea Agent
→ Reflection Agent
→ Aprovação Humana

---

## Etapa 2 - Estruturação

### Objetivo

Construir o blueprint completo do ebook.

### Entrada

Ideia aprovada.

### Saída

* Introdução
* Capítulos
* Objetivos por capítulo
* Tópicos por capítulo
* Conclusão

### Workflow

Outline Agent
→ Reflection Agent
→ Aprovação Humana

---

## Etapa 3 - Desenvolvimento

### Objetivo

Produzir o conteúdo completo do ebook.

### Entrada

Estrutura aprovada.

### Saída

Capítulos completos.

### Workflow

Writer Agent
→ Reflection Agent
→ Aprovação Humana

Cada capítulo será gerado individualmente.

---

## Etapa 4 - Conversão

### Objetivo

Converter o livro final para formatos compatíveis com KDP.

### Entrada

Livro aprovado.

### Saída

* EPUB
* PDF
* DOCX

---

# 4. Human In The Loop

Todas as etapas entre Ideação e Desenvolvimento exigem aprovação humana.

O usuário poderá:

* Aprovar
* Rejeitar
* Editar
* Solicitar nova geração

Nenhum artefato avançará automaticamente sem aprovação.

---

# 5. Reflection Pattern

Cada etapa de geração possuirá um agente de crítica responsável por:

* Detectar inconsistências
* Melhorar clareza
* Melhorar estrutura
* Sugerir refinamentos

O agente de crítica não altera diretamente o resultado.

As sugestões serão apresentadas ao usuário para aprovação.

---

# 6. Arquitetura

## Modelo

Monorepo.

```text
ebook-factory/

apps/
├── frontend
└── backend

packages/
├── workflow-engine
├── ai-agents
├── shared-types
└── kdp-converter

infra/
docs/
```

---

# 7. Stack Tecnológica

## Frontend

* Next.js
* TypeScript
* Tailwind CSS
* Shadcn UI

## Backend

* FastAPI
* Python 3.12+
* LangGraph
* Pydantic

## Banco de Dados

* Supabase Self Hosted
* PostgreSQL

## Cache e Filas

* Redis

## Conversão

* Pandoc

## Containers

* Docker
* Docker Compose

---

# 8. Observabilidade

## Objetivos

Permitir rastreamento completo da execução dos workflows.

### Métricas

* Tempo por etapa
* Tokens consumidos
* Custos
* Erros
* Iterações de reflection
* Aprovações humanas

---

## Observabilidade de IA

### Ferramenta

Langfuse

### Dados monitorados

* Prompts
* Respostas
* Traces
* Spans
* Custos
* Tokens
* Latência

---

## Observabilidade da Plataforma

### Ferramentas

* OpenTelemetry
* Prometheus
* Grafana

### Dados monitorados

* APIs
* Banco de dados
* Redis
* Uso de recursos
* Logs

---

# 9. Persistência

## Entidade Project

```text
Project
├── Workflow
├── Chapters
├── Versions
└── Files
```

### Campos

* id
* title
* status
* created_at
* updated_at

---

## Entidade Chapter

### Campos

* id
* project_id
* title
* content
* version
* status

---

## Entidade Artifact

### Campos

* id
* project_id
* type
* content
* version
* created_at

---

## Entidade Approval

### Campos

* id
* artifact_id
* approved
* feedback
* created_at

---

# 10. Workflow Engine

## Tecnologia

LangGraph

## Estados

```text
IDEATION
STRUCTURING
WRITING
REVIEW
CONVERTING
COMPLETED
```

## Fluxo

START
→ IDEATION
→ STRUCTURING
→ WRITING
→ CONVERTING
→ END

Pontos de aprovação humana interrompem a execução até intervenção do usuário.

---

# 11. Armazenamento de Arquivos

Supabase Storage.

Estrutura:

```text
projects/
├── source/
├── chapters/
├── exports/
│   ├── ebook.epub
│   ├── ebook.pdf
│   └── ebook.docx
```

---

# 12. MVP

## Funcionalidades

* Criação de projeto
* Ideação assistida por IA
* Estruturação assistida por IA
* Geração de capítulos
* Reflection Pattern
* Aprovação humana
* Versionamento
* Exportação EPUB
* Exportação PDF
* Exportação DOCX
* Observabilidade via Langfuse

## Critérios de Sucesso

* Usuário consegue criar um ebook completo.
* Ebook pode ser enviado para Amazon KDP.
* Todas as interações de IA são rastreáveis.
* Todo artefato possui histórico de versões.
* Todo workflow possui pontos de aprovação humana.

```
```
