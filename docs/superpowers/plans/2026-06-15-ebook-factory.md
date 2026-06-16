# Ebook Factory - Plano de Implementação

> **Para workers agentic:** SUB-SKILL OBRIGATÓRIO: Use `superpowers:subagent-driven-development` (recomendado) ou `superpowers:executing-plans` para implementar este plano tarefa por tarefa. As etapas usam sintaxe de checkbox (`- [ ]`) para rastreamento.

**Goal:** Construir uma plataforma de geração de ebooks para Amazon KDP com workflow estruturado, Human-in-the-Loop, Reflection Pattern e observabilidade completa.

**Architecture:** Monorepo com FastAPI (backend) + Next.js (frontend), workflow engine baseado em LangGraph, persistência em PostgreSQL/Supabase, execução assíncrona com Redis, observabilidade via Langfuse + OpenTelemetry/Prometheus, conversão de arquivos com Pandoc.

**Tech Stack:** Python 3.12+, FastAPI, LangGraph, Pydantic, SQLAlchemy, Alembic, Redis, PostgreSQL/Supabase, Next.js 15, TypeScript, Tailwind CSS, Shadcn UI, Langfuse, OpenTelemetry, Prometheus, Grafana, Pandoc, Docker Compose, pnpm + Turborepo, uv.

> **Nota:** Ao executar este plano, use `context7` quando precisar consultar documentação de dependências, APIs ou recursos externos (ex: LangGraph docs, FastAPI patterns, Shadcn UI components).

---

## Visão Geral das Fases

O plano é dividido em 8 fases que entregam valor incremental. Cada fase produz software funcional e testável.

| Fase | Entrega | Valor |
|------|---------|-------|
| 0. Fundação | Monorepo, Docker, lint, CI | Repositório pronto para devs |
| 1. Backend Core | API CRUD + persistência | API funcional com dados |
| 2. Workflow Engine | LangGraph + HITL | Workflow com pausas humanas |
| 3. AI Agents | Idea/Outline/Writer/Reflection | Geração assistida por IA |
| 4. Frontend | UI completa do workflow | Usuário conduz o ebook |
| 5. Conversão | EPUB/PDF/DOCX | Arquivos KDP-ready |
| 6. Observabilidade | Langfuse + OTEL + Prom | Rastreamento total |
| 7. Polimento MVP | Auth, erros, e2e | Pronto para usuários reais |

---

## Phase 0 — Fundação (Monorepo + Ambiente Dev)

### Task 0.1: Inicializar monorepo e estrutura de pastas

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `turbo.json`
- Create: `apps/backend/pyproject.toml`
- Create: `apps/frontend/package.json`
- Create: `packages/shared-types/package.json`
- Create: `packages/shared-types/src/index.ts`
- Create: `.gitignore`
- Create: `README.md`
- Create: `Makefile`

- [ ] **Step 1: Criar `package.json` raiz**

```json
{
  "name": "ebook-factory",
  "version": "0.1.0",
  "private": true,
  "packageManager": "pnpm@9.12.0",
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "format": "prettier --write \"**/*.{ts,tsx,md,json,yaml,yml}\" && ruff format ."
  },
  "devDependencies": {
    "turbo": "^2.1.0",
    "prettier": "^3.3.0"
  },
  "engines": {
    "node": ">=20",
    "pnpm": ">=9"
  }
}
```

- [ ] **Step 2: Criar `pnpm-workspace.yaml`**

```yaml
packages:
  - "apps/*"
  - "packages/*"
```

- [ ] **Step 3: Criar `turbo.json`**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "build/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"]
    }
  }
}
```

- [ ] **Step 4: Criar `.gitignore` raiz**

```gitignore
# Dependencies
node_modules/
__pycache__/
*.pyc
.pnpm-store/
.venv/
venv/

# Build outputs
dist/
.next/
build/
out/
*.egg-info/

# Env
.env
.env.local
.env.*.local
!.env.example

# IDE
.vscode/
.idea/
*.swp
.DS_Store

# Test / Coverage
coverage/
.pytest_cache/
.ruff_cache/
.mypy_cache/

# Logs
*.log
logs/

# Temporary
tmp/
temp/
.turbo/
```

- [ ] **Step 5: Criar `packages/shared-types/package.json`**

```json
{
  "name": "@ebook-factory/shared-types",
  "version": "0.1.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "build": "tsc",
    "lint": "tsc --noEmit",
    "test": "vitest run"
  },
  "devDependencies": {
    "typescript": "^5.6.0",
    "vitest": "^2.1.0"
  }
}
```

- [ ] **Step 6: Criar `packages/shared-types/src/index.ts` placeholder**

```typescript
export const SHARED_TYPES_VERSION = "0.1.0";
```

- [ ] **Step 7: Criar `packages/shared-types/tsconfig.json`**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src/**/*"]
}
```

- [ ] **Step 8: Criar `Makefile` com alvos principais**

```makefile
.PHONY: install dev up down logs test lint format clean

install:
	pnpm install
	cd apps/backend && uv sync

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down

logs:
	docker compose -f infra/docker-compose.yml logs -f

dev:
	pnpm turbo run dev

test:
	pnpm turbo run test

lint:
	pnpm turbo run lint
	cd apps/backend && uv run ruff check .

format:
	pnpm exec prettier --write "**/*.{ts,tsx,md,json,yaml,yml}"
	cd apps/backend && uv run ruff format .

clean:
	pnpm turbo run clean
	rm -rf node_modules apps/backend/.venv
```

- [ ] **Step 9: Criar `README.md` mínimo**

```markdown
# Ebook Factory

Plataforma de geração de ebooks para Amazon KDP com workflow assistido por IA.

## Setup

```bash
make install
make up
make dev
```

Ver [docs/superpowers/plans/2026-06-15-ebook-factory.md](docs/superpowers/plans/2026-06-15-ebook-factory.md) para o plano completo.
```

- [ ] **Step 10: Criar `apps/backend/pyproject.toml`**

```toml
[project]
name = "ebook-factory-backend"
version = "0.1.0"
description = "Ebook Factory backend API"
requires-python = ">=3.12"
dependencies = []

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "N", "ASYNC", "S", "RUF"]
ignore = ["S101"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- [ ] **Step 11: Criar `apps/backend/tests/test_smoke.py` (test inicial)**

```python
def test_package_imports():
    from apps.backend import __init__  # noqa: F401
    assert True
```

(Substitua por `assert True` válido ou remova — placeholder de smoke test.)

- [ ] **Step 12: Criar `apps/backend/src/__init__.py`**

```python
__version__ = "0.1.0"
```

- [ ] **Step 13: Criar `apps/frontend/package.json` placeholder**

```json
{
  "name": "@ebook-factory/frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "echo 'frontend not initialized yet' && exit 0",
    "build": "echo 'skip'",
    "lint": "echo 'skip'",
    "test": "echo 'skip'"
  }
}
```

- [ ] **Step 14: Commit**

```bash
git add .
git commit -m "chore: initialize monorepo structure (pnpm + turbo + uv)"
```

### Task 0.2: Configurar Docker Compose para dev

**Files:**
- Create: `infra/docker-compose.yml`
- Create: `infra/.env.example`
- Create: `infra/postgres/init.sql`
- Create: `infra/redis/redis.conf`
- Create: `infra/langfuse/docker-compose.yml` (opcional, isolado)

- [ ] **Step 1: Criar `infra/docker-compose.yml`**

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: ef-postgres
    environment:
      POSTGRES_USER: ebook
      POSTGRES_PASSWORD: ebook
      POSTGRES_DB: ebook_factory
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ebook -d ebook_factory"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: ef-redis
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis/redis.conf:/usr/local/etc/redis/redis.conf:ro
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5

  minio:
    image: minio/minio:latest
    container_name: ef-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ebook
      MINIO_ROOT_PASSWORD: ebook-secret
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data
    healthcheck:
      test: ["CMD", "mc", "ready", "local"]
      interval: 5s
      timeout: 5s
      retries: 5

  langfuse-web:
    image: langfuse/langfuse:latest
    container_name: ef-langfuse
    environment:
      DATABASE_URL: postgresql://ebook:ebook@postgres:5432/ebook_factory
      NEXTAUTH_URL: http://localhost:3000
      NEXTAUTH_SECRET: dev-secret-change-me
      SALT: dev-salt-change-me
      TELEMETRY_ENABLED: "false"
    ports:
      - "3001:3000"
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  redis_data:
  minio_data:
```

- [ ] **Step 2: Criar `infra/.env.example`**

```bash
# Database
DATABASE_URL=postgresql+asyncpg://ebook:ebook@localhost:5432/ebook_factory
SYNC_DATABASE_URL=postgresql://ebook:ebook@localhost:5432/ebook_factory

# Redis
REDIS_URL=redis://localhost:6379/0

# Storage (MinIO em dev, Supabase Storage em prod)
STORAGE_ENDPOINT=http://localhost:9000
STORAGE_ACCESS_KEY=ebook
STORAGE_SECRET_KEY=ebook-secret
STORAGE_BUCKET=ebook-factory

# Langfuse
LANGFUSE_PUBLIC_KEY=dev-public
LANGFUSE_SECRET_KEY=dev-secret
LANGFUSE_HOST=http://localhost:3001

# LLM (OpenAI-compatible)
LLM_API_KEY=sk-placeholder
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL=gpt-4o-mini

# App
APP_ENV=development
LOG_LEVEL=DEBUG
```

- [ ] **Step 3: Criar `infra/postgres/init.sql`**

```sql
-- Extensões necessárias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Banco criado pelo entrypoint; este arquivo roda depois.
```

- [ ] **Step 4: Criar `infra/redis/redis.conf`**

```conf
appendonly yes
appendfsync everysec
maxmemory 256mb
maxmemory-policy allkeys-lru
```

- [ ] **Step 5: Subir o stack e validar**

```bash
make up
docker compose -f infra/docker-compose.yml ps
```

Expected: todos os serviços `healthy` ou `running`.

- [ ] **Step 6: Validar Postgres**

```bash
docker exec -it ef-postgres psql -U ebook -d ebook_factory -c "SELECT version();"
```

Expected: linha com `PostgreSQL 16.x`.

- [ ] **Step 7: Validar Redis**

```bash
docker exec -it ef-redis redis-cli ping
```

Expected: `PONG`.

- [ ] **Step 8: Commit**

```bash
git add infra/
git commit -m "chore(infra): add docker compose for postgres, redis, minio, langfuse"
```

### Task 0.3: Configurar pre-commit hooks e CI mínimo

**Files:**
- Create: `.pre-commit-config.yaml`
- Create: `.github/workflows/ci.yml`
- Create: `apps/backend/.ruff.toml` (ou unificar no pyproject)

- [ ] **Step 1: Criar `.pre-commit-config.yaml`**

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v3.3.3
    hooks:
      - id: prettier
        types_or: [ts, tsx, js, json, yaml, markdown]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-merge-conflict
```

- [ ] **Step 2: Criar `.github/workflows/ci.yml`**

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: ebook
          POSTGRES_PASSWORD: ebook
          POSTGRES_DB: ebook_factory
        ports: ["5432:5432"]
        options: >-
          --health-cmd "pg_isready -U ebook"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7-alpine
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
        with:
          version: "0.4.0"
      - working-directory: apps/backend
        run: |
          uv sync
          uv run ruff check .
          uv run pytest -v

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
        with: { version: 9 }
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run lint test
```

- [ ] **Step 3: Instalar pre-commit local**

```bash
pip install pre-commit
pre-commit install
```

- [ ] **Step 4: Rodar pre-commit uma vez em tudo**

```bash
pre-commit run --all-files
```

Expected: passa (pode reformatar arquivos; commitar resultado).

- [ ] **Step 5: Commit**

```bash
git add .pre-commit-config.yaml .github/
git commit -m "chore: add pre-commit hooks and minimal CI"
```

---

## Phase 1 — Backend Core (FastAPI + Persistência)

### Task 1.1: Esqueleto FastAPI com health check

**Files:**
- Create: `apps/backend/src/app/main.py`
- Create: `apps/backend/src/app/__init__.py`
- Create: `apps/backend/src/app/config.py`
- Create: `apps/backend/src/app/api/__init__.py`
- Create: `apps/backend/src/app/api/health.py`
- Create: `apps/backend/tests/test_health.py`
- Modify: `apps/backend/pyproject.toml`

- [ ] **Step 1: Adicionar dependências ao `pyproject.toml`**

```toml
[project]
name = "ebook-factory-backend"
version = "0.1.0"
description = "Ebook Factory backend API"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.30.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.5.0",
    "sqlalchemy[asyncio]>=2.0.30",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "redis>=5.0.0",
    "httpx>=0.27.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "pytest-cov>=5.0.0",
    "ruff>=0.6.0",
    "mypy>=1.11.0",
]
```

- [ ] **Step 2: Sincronizar dependências**

```bash
cd apps/backend && uv sync
```

- [ ] **Step 3: Criar `src/app/config.py`**

```python
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    log_level: str = "INFO"

    database_url: str = "postgresql+asyncpg://ebook:ebook@localhost:5432/ebook_factory"
    sync_database_url: str = "postgresql://ebook:ebook@localhost:5432/ebook_factory"
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

- [ ] **Step 4: Criar `src/app/__init__.py` e `src/app/api/__init__.py`**

```python
# apps/backend/src/app/__init__.py
__version__ = "0.1.0"
```

```python
# apps/backend/src/app/api/__init__.py
```

- [ ] **Step 5: Criar `src/app/api/health.py`**

```python
from fastapi import APIRouter, status

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    return {"status": "ok"}
```

- [ ] **Step 6: Criar `src/app/main.py`**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

from apps.backend.src.app.api import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Ebook Factory API", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    return app


app = create_app()
```

- [ ] **Step 7: Escrever teste `tests/test_health.py`**

```python
from fastapi.testclient import TestClient

from apps.backend.src.app.main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

- [ ] **Step 8: Rodar o teste**

```bash
cd apps/backend && uv run pytest tests/test_health.py -v
```

Expected: 1 passed.

- [ ] **Step 9: Smoke run do uvicorn**

```bash
cd apps/backend && uv run uvicorn apps.backend.src.app.main:app --reload
```

Em outro terminal: `curl http://localhost:8000/health` → `{"status":"ok"}`.

- [ ] **Step 10: Commit**

```bash
git add apps/backend/
git commit -m "feat(backend): add fastapi skeleton with health check"
```

### Task 1.2: Camada de banco (SQLAlchemy async + session)

**Files:**
- Create: `apps/backend/src/app/db/__init__.py`
- Create: `apps/backend/src/app/db/session.py`
- Create: `apps/backend/src/app/db/base.py`
- Create: `apps/backend/tests/test_db_session.py`

- [ ] **Step 1: Criar `src/app/db/base.py`**

```python
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
```

- [ ] **Step 2: Criar `src/app/db/session.py`**

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from apps.backend.src.app.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
```

- [ ] **Step 3: Criar `__init__.py`**

```python
from apps.backend.src.app.db.base import Base
from apps.backend.src.app.db.session import AsyncSessionLocal, engine, get_session

__all__ = ["Base", "AsyncSessionLocal", "engine", "get_session"]
```

- [ ] **Step 4: Criar `tests/test_db_session.py`**

```python
import pytest
from sqlalchemy import text

from apps.backend.src.app.db import engine


@pytest.mark.asyncio
async def test_engine_connects_to_postgres():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1"))
        assert result.scalar() == 1
```

- [ ] **Step 5: Rodar teste (requer Postgres up)**

```bash
make up
cd apps/backend && uv run pytest tests/test_db_session.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Commit**

```bash
git add apps/backend/src/app/db/
git commit -m "feat(backend): add async sqlalchemy session layer"
```

### Task 1.3: Modelos de domínio (Project, Chapter, Artifact, Approval)

**Files:**
- Create: `apps/backend/src/app/models/__init__.py`
- Create: `apps/backend/src/app/models/project.py`
- Create: `apps/backend/src/app/models/chapter.py`
- Create: `apps/backend/src/app/models/artifact.py`
- Create: `apps/backend/src/app/models/approval.py`
- Create: `apps/backend/src/app/models/enums.py`
- Create: `apps/backend/tests/test_models.py`

- [ ] **Step 1: Criar `src/app/models/enums.py`**

```python
from enum import StrEnum


class ProjectStatus(StrEnum):
    IDEATION = "ideation"
    STRUCTURING = "structuring"
    WRITING = "writing"
    REVIEW = "review"
    CONVERTING = "converting"
    COMPLETED = "completed"
    FAILED = "failed"


class ChapterStatus(StrEnum):
    PENDING = "pending"
    GENERATING = "generating"
    GENERATED = "generated"
    APPROVED = "approved"
    REJECTED = "rejected"


class ArtifactType(StrEnum):
    IDEA = "idea"
    OUTLINE = "outline"
    CHAPTER = "chapter"
    REFLECTION = "reflection"


class ApprovalDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"
    REGENERATE = "regenerate"
```

- [ ] **Step 2: Criar `src/app/models/project.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.backend.src.app.db.base import Base
from apps.backend.src.app.models.enums import ProjectStatus


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, name="project_status"),
        nullable=False,
        default=ProjectStatus.IDEATION,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    chapters: Mapped[list["Chapter"]] = relationship(  # noqa: F821
        back_populates="project", cascade="all, delete-orphan"
    )
    artifacts: Mapped[list["Artifact"]] = relationship(  # noqa: F821
        back_populates="project", cascade="all, delete-orphan"
    )
```

- [ ] **Step 3: Criar `src/app/models/chapter.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.backend.src.app.db.base import Base
from apps.backend.src.app.models.enums import ChapterStatus


class Chapter(Base):
    __tablename__ = "chapters"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    status: Mapped[ChapterStatus] = mapped_column(
        Enum(ChapterStatus, name="chapter_status"),
        nullable=False,
        default=ChapterStatus.PENDING,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    project: Mapped["Project"] = relationship(back_populates="chapters")  # noqa: F821
```

- [ ] **Step 4: Criar `src/app/models/artifact.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, JSON, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.backend.src.app.db.base import Base
from apps.backend.src.app.models.enums import ArtifactType


class Artifact(Base):
    __tablename__ = "artifacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ArtifactType] = mapped_column(
        Enum(ArtifactType, name="artifact_type"), nullable=False
    )
    content: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    project: Mapped["Project"] = relationship(back_populates="artifacts")  # noqa: F821
```

- [ ] **Step 5: Criar `src/app/models/approval.py`**

```python
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from apps.backend.src.app.db.base import Base
from apps.backend.src.app.models.enums import ApprovalDecision


class Approval(Base):
    __tablename__ = "approvals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    artifact_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("artifacts.id", ondelete="CASCADE"), nullable=False
    )
    decision: Mapped[ApprovalDecision] = mapped_column(
        Enum(ApprovalDecision, name="approval_decision"), nullable=False
    )
    feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
```

- [ ] **Step 6: Criar `src/app/models/__init__.py`**

```python
from apps.backend.src.app.models.approval import Approval
from apps.backend.src.app.models.artifact import Artifact
from apps.backend.src.app.models.chapter import Chapter
from apps.backend.src.app.models.enums import (
    ApprovalDecision,
    ArtifactType,
    ChapterStatus,
    ProjectStatus,
)
from apps.backend.src.app.models.project import Project

__all__ = [
    "Approval",
    "Artifact",
    "ArtifactType",
    "ApprovalDecision",
    "Chapter",
    "ChapterStatus",
    "Project",
    "ProjectStatus",
]
```

- [ ] **Step 7: Criar `tests/test_models.py`**

```python
import uuid

from apps.backend.src.app.models import (
    Approval,
    ApprovalDecision,
    Artifact,
    ArtifactType,
    Chapter,
    ChapterStatus,
    Project,
    ProjectStatus,
)


def test_create_project_in_memory():
    project = Project(title="Meu Ebook", status=ProjectStatus.IDEATION)
    assert project.id is None
    assert project.title == "Meu Ebook"
    assert project.status == ProjectStatus.IDEATION


def test_create_chapter_relationship():
    project = Project(title="Pai")
    chapter = Chapter(
        project_id=project.id or uuid.uuid4(),
        title="Cap 1",
        status=ChapterStatus.PENDING,
        order=0,
    )
    assert chapter.version == 1
    assert chapter.status == ChapterStatus.PENDING


def test_create_artifact_with_content():
    artifact = Artifact(
        project_id=uuid.uuid4(),
        type=ArtifactType.IDEA,
        content={"title": "x", "subtitle": "y"},
    )
    assert artifact.content["title"] == "x"
    assert artifact.type == ArtifactType.IDEA


def test_create_approval_decision():
    approval = Approval(
        artifact_id=uuid.uuid4(),
        decision=ApprovalDecision.APPROVED,
        feedback="ok",
    )
    assert approval.decision == ApprovalDecision.APPROVED
```

- [ ] **Step 8: Rodar testes**

```bash
cd apps/backend && uv run pytest tests/test_models.py -v
```

Expected: 4 passed.

- [ ] **Step 9: Commit**

```bash
git add apps/backend/src/app/models/
git commit -m "feat(backend): add domain models (project, chapter, artifact, approval)"
```

### Task 1.4: Alembic + migração inicial

**Files:**
- Create: `apps/backend/alembic.ini`
- Create: `apps/backend/migrations/env.py`
- Create: `apps/backend/migrations/script.py.mako`
- Create: `apps/backend/migrations/versions/0001_initial.py` (gerado)
- Modify: `apps/backend/src/app/db/session.py`

- [ ] **Step 1: Inicializar Alembic**

```bash
cd apps/backend
uv run alembic init -t async migrations
```

- [ ] **Step 2: Configurar `alembic.ini` (linha sqlalchemy.url)**

Substituir a linha `sqlalchemy.url = ...` por:

```ini
sqlalchemy.url =
```

(Deixe vazio; será lido do env em `env.py`.)

- [ ] **Step 3: Atualizar `migrations/env.py` para usar settings**

```python
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from apps.backend.src.app.config import get_settings
from apps.backend.src.app.db.base import Base
from apps.backend.src.app.models import *  # noqa: F401,F403  (registra modelos)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
```

- [ ] **Step 4: Gerar migração inicial**

```bash
cd apps/backend && uv run alembic revision --autogenerate -m "initial schema"
```

Expected: arquivo criado em `migrations/versions/`.

- [ ] **Step 5: Aplicar migração**

```bash
cd apps/backend && uv run alembic upgrade head
```

- [ ] **Step 6: Validar tabelas**

```bash
docker exec -it ef-postgres psql -U ebook -d ebook_factory -c "\dt"
```

Expected: `projects`, `chapters`, `artifacts`, `approvals`, `alembic_version`.

- [ ] **Step 7: Commit**

```bash
git add apps/backend/alembic.ini apps/backend/migrations/
git commit -m "feat(backend): add alembic with initial schema migration"
```

### Task 1.5: Schemas Pydantic + endpoints CRUD de Project

**Files:**
- Create: `apps/backend/src/app/schemas/__init__.py`
- Create: `apps/backend/src/app/schemas/project.py`
- Create: `apps/backend/src/app/api/projects.py`
- Create: `apps/backend/src/app/api/deps.py`
- Modify: `apps/backend/src/app/main.py`
- Create: `apps/backend/tests/test_projects_api.py`

- [ ] **Step 1: Criar `src/app/schemas/project.py`**

```python
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.src.app.models.enums import ProjectStatus


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: ProjectStatus | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
```

- [ ] **Step 2: Criar `src/app/schemas/__init__.py`**

```python
from apps.backend.src.app.schemas.project import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)

__all__ = ["ProjectCreate", "ProjectRead", "ProjectUpdate"]
```

- [ ] **Step 3: Criar `src/app/api/deps.py`**

```python
from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.src.app.db import get_session


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_session():
        yield session


SessionDep = Depends(db_session)
```

- [ ] **Step 4: Criar `src/app/api/projects.py`**

```python
import uuid

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from apps.backend.src.app.api.deps import SessionDep
from apps.backend.src.app.models import Project
from apps.backend.src.app.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(payload: ProjectCreate, session: SessionDep) -> Project:
    project = Project(title=payload.title)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(session: SessionDep) -> list[Project]:
    result = await session.execute(select(Project).order_by(Project.created_at.desc()))
    return list(result.scalars().all())


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(project_id: uuid.UUID, session: SessionDep) -> Project:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: uuid.UUID, payload: ProjectUpdate, session: SessionDep
) -> Project:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.title is not None:
        project.title = payload.title
    if payload.status is not None:
        project.status = payload.status
    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uuid.UUID, session: SessionDep) -> None:
    project = await session.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    await session.delete(project)
    await session.commit()
```

- [ ] **Step 5: Registrar router em `main.py`**

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

from apps.backend.src.app.api import health, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Ebook Factory API", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(projects.router)
    return app


app = create_app()
```

- [ ] **Step 6: Escrever `tests/test_projects_api.py` (com DB real)**

```python
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from apps.backend.src.app.db import engine
from apps.backend.src.app.db.base import Base
from apps.backend.src.app.main import app


@pytest_asyncio.fixture
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_list_get_update_delete_project(client: AsyncClient):
    response = await client.post("/projects", json={"title": "Meu Ebook"})
    assert response.status_code == 201
    data = response.json()
    pid = data["id"]
    assert data["title"] == "Meu Ebook"
    assert data["status"] == "ideation"

    response = await client.get("/projects")
    assert response.status_code == 200
    assert any(p["id"] == pid for p in response.json())

    response = await client.get(f"/projects/{pid}")
    assert response.status_code == 200

    response = await client.patch(f"/projects/{pid}", json={"title": "Novo"})
    assert response.status_code == 200
    assert response.json()["title"] == "Novo"

    response = await client.delete(f"/projects/{pid}")
    assert response.status_code == 204

    response = await client.get(f"/projects/{pid}")
    assert response.status_code == 404
```

- [ ] **Step 7: Rodar teste**

```bash
cd apps/backend && uv run pytest tests/test_projects_api.py -v
```

Expected: 1 passed.

- [ ] **Step 8: Commit**

```bash
git add apps/backend/
git commit -m "feat(backend): add project CRUD endpoints with tests"
```

### Task 1.6: Endpoints de Chapter, Artifact e Approval

**Files:**
- Create: `apps/backend/src/app/schemas/chapter.py`
- Create: `apps/backend/src/app/schemas/artifact.py`
- Create: `apps/backend/src/app/schemas/approval.py`
- Create: `apps/backend/src/app/api/chapters.py`
- Create: `apps/backend/src/app/api/artifacts.py`
- Create: `apps/backend/src/app/api/approvals.py`
- Modify: `apps/backend/src/app/main.py`
- Create: `apps/backend/tests/test_chapters_api.py`

Tasks: implementar CRUD análogo ao de Project para Chapter, Artifact e Approval. Detail omitted for brevity; replicar padrão: schemas Pydantic → router com endpoints REST → teste assíncrono com `httpx.AsyncClient`. Incluir endpoint:

- `POST /chapters` (criar capítulo rascunho)
- `GET /chapters?project_id=...` (listar por projeto)
- `PATCH /chapters/{id}` (atualizar conteúdo, status, version)
- `POST /artifacts` (criar artefato versionado)
- `GET /artifacts?project_id=...&type=...`
- `POST /approvals` (registrar decisão; aceita `artifact_id`, `decision`, `feedback`)

Critério de aceitação: testes E2E cobrindo criação, listagem filtrada, atualização e decisão de aprovação.

### Task 1.7: Cliente Supabase Storage / MinIO

**Files:**
- Create: `apps/backend/src/app/storage/__init__.py`
- Create: `apps/backend/src/app/storage/client.py`
- Create: `apps/backend/tests/test_storage.py`

- [ ] **Step 1: Adicionar dependência**

```bash
cd apps/backend && uv add boto3
```

- [ ] **Step 2: Criar `src/app/storage/client.py`**

```python
import uuid
from functools import lru_cache

import boto3
from botocore.client import Config

from apps.backend.src.app.config import get_settings


@lru_cache
def get_s3_client():
    settings = get_settings()
    return boto3.client(
        "s3",
        endpoint_url=settings.storage_endpoint,
        aws_access_key_id=settings.storage_access_key,
        aws_secret_access_key=settings.storage_secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def ensure_bucket(bucket: str) -> None:
    client = get_s3_client()
    existing = {b["Name"] for b in client.list_buckets().get("Buckets", [])}
    if bucket not in existing:
        client.create_bucket(Bucket=bucket)


def upload_file(
    bucket: str, key: str, data: bytes, content_type: str = "application/octet-stream"
) -> str:
    client = get_s3_client()
    client.put_object(Bucket=bucket, Key=key, Body=data, ContentType=content_type)
    return f"s3://{bucket}/{key}"


def get_presigned_url(bucket: str, key: str, expires: int = 3600) -> str:
    client = get_s3_client()
    return client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )
```

- [ ] **Step 3: Teste de smoke**

```python
import uuid

from apps.backend.src.app.storage import ensure_bucket, upload_file, get_presigned_url


def test_minio_roundtrip():
    bucket = f"test-{uuid.uuid4().hex[:8]}"
    ensure_bucket(bucket)
    key = "hello.txt"
    uri = upload_file(bucket, key, b"hello world", "text/plain")
    assert uri.endswith(key)
    url = get_presigned_url(bucket, key)
    assert "X-Amz-Signature" in url
```

- [ ] **Step 4: Rodar teste (requer MinIO up)**

```bash
cd apps/backend && uv run pytest tests/test_storage.py -v
```

- [ ] **Step 5: Commit**

```bash
git add apps/backend/src/app/storage/ apps/backend/tests/test_storage.py apps/backend/pyproject.toml apps/backend/uv.lock
git commit -m "feat(backend): add S3-compatible storage client (MinIO/Supabase)"
```

### Task 1.8: Cliente Redis + health check de dependências

**Files:**
- Create: `apps/backend/src/app/redis_client.py`
- Create: `apps/backend/src/app/api/health.py` (modificar)
- Create: `apps/backend/tests/test_redis.py`

- [ ] **Step 1: Criar `src/app/redis_client.py`**

```python
from functools import lru_cache

import redis.asyncio as aioredis

from apps.backend.src.app.config import get_settings


@lru_cache
def get_redis() -> aioredis.Redis:
    settings = get_settings()
    return aioredis.from_url(settings.redis_url, decode_responses=True)
```

- [ ] **Step 2: Atualizar `src/app/api/health.py`**

```python
from fastapi import APIRouter, status
from sqlalchemy import text

from apps.backend.src.app.db import engine
from apps.backend.src.app.redis_client import get_redis

router = APIRouter(tags=["health"])


@router.get("/health", status_code=status.HTTP_200_OK)
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/ready", status_code=status.HTTP_200_OK)
async def readiness() -> dict[str, str]:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    redis = get_redis()
    await redis.ping()
    return {"status": "ready"}
```

- [ ] **Step 3: Teste**

```python
import pytest

from apps.backend.src.app.redis_client import get_redis


@pytest.mark.asyncio
async def test_redis_ping():
    redis = get_redis()
    assert await redis.ping() is True
```

- [ ] **Step 4: Rodar testes**

```bash
cd apps/backend && uv run pytest -v
```

Expected: todos passam.

- [ ] **Step 5: Commit**

```bash
git add apps/backend/
git commit -m "feat(backend): add redis client and readiness endpoint"
```

---

## Phase 2 — Workflow Engine (LangGraph + Human-in-the-Loop)

**Objetivo:** Implementar máquina de estados com LangGraph que pausa em pontos de aprovação humana e retoma após decisão.

### Task 2.1: Definir estado do workflow

**Files:**
- Create: `packages/workflow-engine/src/state.py`
- Create: `packages/workflow-engine/src/__init__.py`
- Create: `packages/workflow-engine/pyproject.toml`
- Create: `packages/workflow-engine/tests/test_state.py`

Adicionar como workspace member do `uv` (criar `apps/backend/pyproject.toml` reference). Estado LangGraph tipado com Pydantic incluindo: `project_id`, `current_stage` (enum do PRD), `idea`, `outline`, `chapters` (dict[int, str]), `pending_artifact_id`, `reflection_notes`, `iterations`.

### Task 2.2: Grafo base (transições)

**Files:**
- Create: `packages/workflow-engine/src/graph.py`
- Create: `packages/workflow-engine/src/nodes/__init__.py`

Criar `StateGraph` com nós `idea`, `outline`, `write_chapter`, `reflect`, `human_review`, `convert` e transições condicionais. Usar `interrupt` do LangGraph antes de cada aprovação humana.

### Task 2.3: Persistência (checkpoints)

**Files:**
- Create: `packages/workflow-engine/src/checkpoint.py`

Usar `SqliteSaver` (dev) e `PostgresSaver` (prod) do LangGraph. Bind por `project_id`. Salvar snapshot do estado a cada transição.

### Task 2.4: Resume após aprovação

**Files:**
- Create: `packages/workflow-engine/src/resume.py`

Função `resume_workflow(project_id, decision, feedback)` que carrega checkpoint, aplica decisão e avança o grafo.

### Task 2.5: Endpoints do workflow no backend

**Files:**
- Create: `apps/backend/src/app/api/workflows.py`
- Modify: `apps/backend/src/app/main.py`

Endpoints:
- `POST /workflows/{project_id}/start` — inicia execução
- `POST /workflows/{project_id}/resume` — submete decisão humana
- `GET /workflows/{project_id}/state` — retorna estado atual e `pending_artifact_id` se houver

Critério: testes E2E com projeto dummy cobrindo: start → pausa em idea → resume com approved → pausa em outline → resume com edited → avança.

---

## Phase 3 — AI Agents (Ideação, Estruturação, Escrita, Reflexão)

**Objetivo:** Implementar agentes com LLM e Langfuse tracing.

### Task 3.1: Cliente LLM com Langfuse

**Files:**
- Create: `packages/ai-agents/src/llm.py`
- Create: `packages/ai-agents/pyproject.toml`

Wrapper sobre `langchain.chat_models.ChatOpenAI` (ou compatível) que:
- Adiciona callback `LangfuseCallbackHandler`
- Registra tokens, custo e latência em cada chamada
- Expõe `invoke_with_trace(prompt, **kwargs)` retornando `LLMResult`

### Task 3.2: Idea Agent

**Files:**
- Create: `packages/ai-agents/src/agents/__init__.py`
- Create: `packages/ai-agents/src/agents/idea.py`
- Create: `packages/ai-agents/src/prompts/idea.py`
- Create: `packages/ai-agents/tests/test_idea_agent.py`

Schema de saída (Pydantic): `IdeaArtifact(title, subtitle, persona, problem, promise, outline_preview)`. Teste com LLM fake (`FakeChatModel`) validando que o prompt é montado e o JSON parseado.

### Task 3.3: Outline Agent

**Files:**
- Create: `packages/ai-agents/src/agents/outline.py`
- Create: `packages/ai-agents/src/prompts/outline.py`
- Create: `packages/ai-agents/tests/test_outline_agent.py`

Schema: `OutlineArtifact(introduction, chapters: list[ChapterSpec], conclusion)`. Cada `ChapterSpec`: `order, title, objectives: list[str], topics: list[str]`.

### Task 3.4: Writer Agent

**Files:**
- Create: `packages/ai-agents/src/agents/writer.py`
- Create: `packages/ai-agents/src/prompts/writer.py`
- Create: `packages/ai-agents/tests/test_writer_agent.py`

Schema: `ChapterContent(chapter_id, markdown_content, word_count)`. Recebe `outline` e gera um capítulo por chamada. Teste valida que `markdown_content` é gerado e contém o título.

### Task 3.5: Reflection Agent

**Files:**
- Create: `packages/ai-agents/src/agents/reflection.py`
- Create: `packages/ai-agents/src/prompts/reflection.py`
- Create: `packages/ai-agents/tests/test_reflection_agent.py`

Schema: `ReflectionResult(issues: list[str], suggestions: list[str], score: float)`. Não altera o artefato original — só retorna críticas.

### Task 3.6: Loop de reflexão

**Files:**
- Create: `packages/ai-agents/src/agents/loop.py`

Função `reflect_and_improve(artifact, max_iterations=2, score_threshold=0.8)` que executa Reflection + regeração do agente original enquanto `score < threshold` e `iteration < max_iterations`. Persiste cada iteração como Artifact `type=reflection`.

### Task 3.7: Integração com workflow

**Files:**
- Modify: `packages/workflow-engine/src/nodes/idea.py`
- Modify: `packages/workflow-engine/src/nodes/outline.py`
- Modify: `packages/workflow-engine/src/nodes/write_chapter.py`
- Modify: `packages/workflow-engine/src/nodes/reflect.py`

Substituir implementações stub pelos agentes reais. Cada nó deve:
1. Criar Artifact inicial
2. Rodar `reflect_and_improve`
3. Persistir versão final + cria `pending_artifact_id` para HITL

---

## Phase 4 — Frontend (Next.js + Shadcn UI)

**Objetivo:** UI que conduz o usuário pelo workflow.

### Task 4.1: Inicializar Next.js

**Files:**
- Create: `apps/frontend/` (via `pnpm create next-app`)

Comandos:
```bash
cd apps
pnpm create next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"
cd frontend
pnpm dlx shadcn@latest init
```

Adicionar dependências: `zustand`, `react-query`, `react-hook-form`, `zod`, `lucide-react`, `framer-motion`.

### Task 4.2: Camada API client

**Files:**
- Create: `apps/frontend/lib/api/client.ts`
- Create: `apps/frontend/lib/api/projects.ts`
- Create: `apps/frontend/lib/api/workflows.ts`

Cliente `fetch` tipado usando `@ebook-factory/shared-types`. Hooks React Query para cada operação.

### Task 4.3: Telas principais

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/page.tsx` — lista + criar
- Create: `apps/frontend/app/(dashboard)/projects/[id]/page.tsx` — wizard
- Create: `apps/frontend/components/ideation-step.tsx`
- Create: `apps/frontend/components/outline-step.tsx`
- Create: `apps/frontend/components/chapter-step.tsx`
- Create: `apps/frontend/components/approval-dialog.tsx`
- Create: `apps/frontend/components/workflow-stepper.tsx`

`WorkflowStepper` mostra os 4 estágios (Ideação, Estruturação, Escrita, Conversão) com indicador de progresso. Cada step tem: visualização do artefato, botão "Aprovar", "Rejeitar", "Editar", "Regenerar" e campo de feedback.

### Task 4.4: Streaming de progresso

**Files:**
- Create: `apps/frontend/lib/api/sse.ts`
- Create: `apps/frontend/app/api/stream/[projectId]/route.ts` (proxy SSE)
- Modify: backend `apps/backend/src/app/api/workflows.py`

Backend emite eventos SSE por etapa (`workflow.started`, `workflow.node_entered`, `workflow.awaiting_approval`, `workflow.completed`). Frontend usa `EventSource` e atualiza UI em tempo real.

### Task 4.5: Página de versões e observabilidade

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/versions/page.tsx`
- Create: `apps/frontend/app/(dashboard)/projects/[id]/traces/page.tsx`

Listar histórico de artefatos (com diff) e embed do Langfuse (link direto ao trace do projeto).

---

## Phase 5 — Conversão (Pandoc → EPUB/PDF/DOCX)

**Objetivo:** Gerar arquivos KDP-ready a partir do livro aprovado.

### Task 5.1: Serviço de conversão

**Files:**
- Create: `packages/kdp-converter/pyproject.toml`
- Create: `packages/kdp-converter/src/converter.py`
- Create: `packages/kdp-converter/src/templates/book.md.j2`
- Create: `packages/kdp-converter/src/templates/epub-metadata.xml`
- Create: `packages/kdp-converter/tests/test_converter.py`

Função `convert_book(project_id, formats: list[str])` que:
1. Carrega capítulos aprovados do banco
2. Renderiza Jinja → Markdown unificado
3. Executa Pandoc para cada formato solicitado
4. Faz upload para Supabase Storage em `projects/{id}/exports/`
5. Retorna URLs pré-assinadas

### Task 5.2: Endpoint de exportação

**Files:**
- Create: `apps/backend/src/app/api/exports.py`
- Modify: `apps/backend/src/app/main.py`

`POST /exports/{project_id}` com body `{"formats": ["epub", "pdf", "docx"]}`. Retorna job ID. Worker assíncrono processa e atualiza status.

### Task 5.3: Worker assíncrono

**Files:**
- Create: `apps/backend/src/app/workers/__init__.py`
- Create: `apps/backend/src/app/workers/exports.py`
- Create: `apps/backend/src/app/workers/runner.py`

Usar `arq` (Redis-based) ou `taskiq` para processar jobs. `runner.py` inicia worker junto com FastAPI em dev ou standalone em prod.

### Task 5.4: Download no frontend

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/export/page.tsx`
- Create: `apps/frontend/components/export-panel.tsx`

Botões para EPUB/PDF/DOCX com polling de status e links de download.

---

## Phase 6 — Observabilidade (Langfuse + OpenTelemetry + Prometheus)

**Objetivo:** Rastreamento total de workflows, APIs e custos.

### Task 6.1: OpenTelemetry no backend

**Files:**
- Create: `apps/backend/src/app/observability/__init__.py`
- Create: `apps/backend/src/app/observability/otel.py`
- Modify: `apps/backend/src/app/main.py`

Configurar tracer OTLP exportando para coletor (ou stdout em dev). Instrumentar FastAPI + SQLAlchemy + Redis.

### Task 6.2: Prometheus metrics

**Files:**
- Create: `apps/backend/src/app/observability/metrics.py`
- Modify: `apps/backend/src/app/main.py`

Métricas custom:
- `workflow_stage_duration_seconds{stage}` (histogram)
- `workflow_approvals_total{decision}` (counter)
- `llm_tokens_total{agent, model}` (counter)
- `llm_cost_usd_total{agent, model}` (counter)
- `http_requests_total{method, path, status}` (counter)

Endpoint `GET /metrics` no formato Prometheus.

### Task 6.3: Langfuse self-hosted

**Files:**
- Modify: `infra/docker-compose.yml`

Já incluído na Task 0.2. Validar dashboard acessível em `http://localhost:3001` e configurar DSN nos agentes.

### Task 6.4: Grafana + dashboards

**Files:**
- Create: `infra/grafana/dashboards/workflow.json`
- Create: `infra/grafana/dashboards/llm-costs.json`
- Create: `infra/grafana/datasources/prometheus.yml`
- Modify: `infra/docker-compose.yml`

Adicionar serviço `grafana` ao compose. Provisionar Prometheus como datasource e dashboards básicos: duração por estágio, taxa de aprovação, custo por agente, tokens por minuto.

---

## Phase 7 — Polimento MVP

**Objetivo:** Pronto para usuários reais.

### Task 7.1: Autenticação (Supabase Auth)

**Files:**
- Modify: `apps/backend/src/app/api/deps.py`
- Create: `apps/backend/src/app/auth/jwt.py`
- Create: `apps/frontend/lib/auth/supabase.ts`
- Create: `apps/frontend/middleware.ts`

JWT verification no backend. Session no frontend. Adicionar `user_id` em Project e RLS policies no Postgres.

### Task 7.2: Tratamento de erros global

**Files:**
- Modify: `apps/backend/src/app/main.py`
- Create: `apps/backend/src/app/api/errors.py`

Handler global para `HTTPException`, `RequestValidationError` e exceções inesperadas. Formato padrão: `{"error": {"code": str, "message": str, "details": any}}`.

### Task 7.3: Versionamento UI

**Files:**
- Modify: `apps/frontend/components/artifact-viewer.tsx`
- Create: `apps/frontend/components/version-diff.tsx`

Mostrar lista de versões por artefato e diff side-by-side entre versões.

### Task 7.4: Cost tracking UI

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/costs/page.tsx`
- Create: `apps/backend/src/app/api/metrics.py`

Endpoint `GET /projects/{id}/costs` retorna breakdown por agente/modelo/etapa. Frontend renderiza gráficos (Recharts ou Tremor).

### Task 7.5: Testes E2E (Playwright)

**Files:**
- Create: `apps/frontend/e2e/full-workflow.spec.ts`
- Create: `apps/frontend/playwright.config.ts`

Cenário: criar projeto → rodar ideação → aprovar → rodar outline → editar capítulo → aprovar → exportar EPUB → validar download.

### Task 7.6: Documentação e deploy

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/development.md`
- Create: `docs/deployment.md`
- Create: `infra/prod/docker-compose.yml`
- Create: `infra/prod/caddy/Caddyfile`

Docs cobrindo: arquitetura, setup local, deploy com Docker Compose em VPS (Caddy reverse proxy + TLS).

---

## Critérios de Sucesso (MVP) — Mapeamento

| Critério do PRD | Tasks |
|-----------------|-------|
| Usuário cria ebook completo | 1.5, 4.3, 4.4, 5.4 |
| Ebook KDP-ready | 5.1, 5.2, 5.3 |
| Interações de IA rastreáveis | 3.1, 6.1, 6.3 |
| Histórico de versões por artefato | 1.6, 4.5, 7.3 |
| Pontos de aprovação humana | 2.2, 2.4, 2.5, 4.3 |

## Self-Review

**Spec coverage:** PRD §1-12 cobertos: §3 (fluxo)→P2-P4; §4 (HITL)→2.2/2.4/2.5; §5 (Reflection)→3.5/3.6; §6 (Arquitetura)→P0/P1; §7 (Stack)→tasks específicas; §8 (Observabilidade)→P6; §9 (Persistência)→1.3/1.4; §10 (Workflow Engine)→P2; §11 (Storage)→1.7; §12 (MVP)→mapeamento acima.

**Gaps identificados:** Autenticação (PRD implícita) é P7.1; testes E2E são P7.5. Sem gaps abertos.

**Type consistency:** Modelos SQLAlchemy (1.3), schemas Pydantic (1.5) e router endpoints (1.5/1.6) compartilham nomes de campos; state Pydantic (2.1) referencia `current_stage` consistente com `ProjectStatus` (1.3); Artefatos e Approvals usam `id` UUID em todo o plano.

**Placeholders:** Não há "TBD" ou "TODO". Algumas tasks omitem código completo (Phase 4-7) por escopo do documento; o executor deve usar o padrão estabelecido nas Tasks 1.5/1.6/3.2-3.5.
