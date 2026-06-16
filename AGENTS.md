# AGENTS.md

## Project Status

**Fase:** Inicial (Pré-desenvolvimento)

O repositório contém apenas o PRD (`PRD.md`) e o plano de implementação (`docs/superpowers/plans/2026-06-15-ebook-factory.md`). Nenhum código foi escrito ainda.

## Estrutura Futura (Monorepo)

A implementação seguirá esta estrutura definida no PRD:

```
ebook-factory/
├── apps/
│   ├── frontend/          # Next.js + Tailwind + Shadcn UI
│   └── backend/           # FastAPI + SQLAlchemy + LangGraph
├── packages/
│   ├── workflow-engine/   # LangGraph state machine + HITL
│   ├── ai-agents/         # LLM agents (Idea, Outline, Writer, Reflection)
│   ├── shared-types/      # TypeScript types compartilhados
│   └── kdp-converter/     # Pandoc EPUB/PDF/DOCX conversion
├── infra/                 # Docker Compose (Postgres, Redis, MinIO, Langfuse, Grafana)
├── docs/
│   └── superpowers/plans/ # Planos de implementação
└── .github/workflows/     # CI
```

## Tech Stack

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

## Setup Commands

```bash
make install       # pnpm install + uv sync
make up            # docker compose up -d (Postgres, Redis, MinIO, Langfuse)
make dev           # turbo run dev (backend + frontend)
make test          # turbo run test
make lint          # turbo run lint + ruff check
make format        # prettier + ruff format
make down          # docker compose down
```

## Planos de Implementação

Ver `docs/superpowers/plans/2026-06-15-ebook-factory.md` para o plano completo dividido em 8 fases.

Sempre consulte o plano antes de começar uma nova tarefa. O plano usa TDD: escreva o teste, veja falhar, implemente, veja passar, commit.

## Convenções

### Backend (Python)

- Async/await em toda a camada de banco e API
- Pydantic v2 para schemas de request/response
- SQLAlchemy 2.0 style (Mapped, mapped_column)
- Testes com pytest + pytest-asyncio + httpx.AsyncClient
- Ruff para lint e formatação (line-length=100)
- Alembic para migrações

### Frontend (TypeScript)

- Next.js App Router
- Server components por padrão, client components só quando necessário
- Shadcn UI para componentes de interface
- React Query para data fetching
- Zustand para estado global
- Zod para validação de formulários
- Testes com Vitest + Playwright (e2e)

### Git

- Branch padrão: `main`
- Commits frequentes por task (2-5 minutos de trabalho)
- Mensagens de commit em inglês, estilo conventional commits (feat, fix, chore, docs)
- Tags: `feat(backend):`, `feat(frontend):`, `chore(infra):`, etc.

## Observação Importante

Toda etapa de geração de IA possui um Reflection Agent que critica o resultado antes de apresentar ao usuário. Nada avança sem aprovação humana (Human-in-the-Loop). Isso é requisito de domínio, não uma decisão técnica — sempre preserve esse fluxo.
