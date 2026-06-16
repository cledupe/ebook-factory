# Ebook Factory

Plataforma de geração de ebooks para publicação na Amazon KDP utilizando Inteligência Artificial e Human-in-the-Loop.

O sistema conduz o usuário desde a ideação do livro até a geração de arquivos compatíveis com a Amazon KDP, com workflow estruturado, iterativo e auditável.

## Fluxo

O processo é dividido em 4 etapas, cada uma com geração por IA, crítica por Reflection Agent e aprovação humana obrigatória:

1. **Ideação** — Nicho, tema e público-alvo geram título, subtítulo, persona e sumário preliminar
2. **Estruturação** — Blueprint completo com introdução, capítulos, objetivos e tópicos
3. **Desenvolvimento** — Conteúdo completo do ebook, capítulo por capítulo
4. **Conversão** — Exportação para EPUB, PDF e DOCX compatíveis com KDP

> **Importante:** Nenhum artefato avança sem aprovação humana. Toda etapa possui um Reflection Agent que critica o resultado antes de apresentá-lo ao usuário.

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Frontend | Next.js 15, TypeScript, Tailwind CSS, Shadcn UI |
| Backend | Python 3.12+, FastAPI, LangGraph, Pydantic, SQLAlchemy |
| Database | PostgreSQL 16 + Supabase (self-hosted) |
| Cache/Queue | Redis 7 |
| Storage | MinIO (dev) / Supabase Storage (prod) |
| Observability | Langfuse, OpenTelemetry, Prometheus, Grafana |
| Conversion | Pandoc |
| Packages | pnpm + Turborepo (JS), uv (Python) |
| Infrastructure | Docker Compose |

## Estrutura do Projeto

```
ebook-factory/
├── apps/
│   ├── frontend/          # Next.js + Tailwind + Shadcn UI
│   └── backend/           # FastAPI + SQLAlchemy + LangGraph
├── packages/
│   ├── workflow-engine/   # LangGraph state machine + HITL
│   ├── ai-agents/         # LLM agents
│   ├── shared-types/      # TypeScript types compartilhados
│   └── kdp-converter/     # Pandoc conversion
├── infra/                 # Docker Compose
├── docs/
│   └── superpowers/plans/ # Planos de implementação
└── .github/workflows/     # CI
```

## Setup

```bash
# Install dependencies
make install

# Start infrastructure (Postgres, Redis, MinIO, Langfuse)
make up

# Start development servers (backend + frontend)
make dev

# Run tests
make test

# Lint and format
make lint
make format

# Stop infrastructure
make down
```

## Status do Projeto

> **Fase:** Inicial (Pré-desenvolvimento)

O repositório contém o PRD, o plano de implementação e o `AGENTS.md`. O desenvolvimento segue o plano em `docs/superpowers/plans/2026-06-15-ebook-factory.md`, organizado em 8 fases com TDD.
