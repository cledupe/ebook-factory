# Task 1: Backend Core (FastAPI + Persistência)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 1 — Backend Core
> **Tasks:** 1.1 a 1.8

---

## Task 1.1: Esqueleto FastAPI com health check

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

---

## Task 1.2: Camada de banco (SQLAlchemy async + session)

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

---

## Task 1.3: Modelos de domínio (Project, Chapter, Artifact, Approval)

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

---

## Task 1.4: Alembic + migração inicial

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

---

## Task 1.5: Schemas Pydantic + endpoints CRUD de Project

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

---

## Task 1.6: Endpoints de Chapter, Artifact e Approval

**Files:**
- Create: `apps/backend/src/app/schemas/chapter.py`
- Create: `apps/backend/src/app/schemas/artifact.py`
- Create: `apps/backend/src/app/schemas/approval.py`
- Create: `apps/backend/src/app/api/chapters.py`
- Create: `apps/backend/src/app/api/artifacts.py`
- Create: `apps/backend/src/app/api/approvals.py`
- Modify: `apps/backend/src/app/main.py`
- Create: `apps/backend/tests/test_chapters_api.py`

- [ ] **Implementar CRUD análogo ao de Project (Task 1.5) para Chapter, Artifact e Approval. Replicar o padrão: schemas Pydantic -> router com endpoints REST -> teste assíncrono com httpx.AsyncClient.**

**Endpoints:**
- `POST /chapters` — criar capítulo rascunho
- `GET /chapters?project_id=...` — listar por projeto
- `PATCH /chapters/{id}` — atualizar conteúdo, status, version
- `POST /artifacts` — criar artefato versionado
- `GET /artifacts?project_id=...&type=...` — listar artefatos (filtráveis)
- `POST /approvals` — registrar decisão (`artifact_id`, `decision`, `feedback`)

**Exemplo de schema para Chapter:**

```python
# apps/backend/src/app/schemas/chapter.py
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from apps.backend.src.app.models.enums import ChapterStatus


class ChapterCreate(BaseModel):
    project_id: uuid.UUID
    title: str = Field(min_length=1, max_length=255)
    order: int = 0


class ChapterUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    status: ChapterStatus | None = None
    version: int | None = None


class ChapterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    content: str | None
    order: int
    version: int
    status: ChapterStatus
    created_at: datetime
    updated_at: datetime
```

- [ ] **Commit**

```bash
git add apps/backend/
git commit -m "feat(backend): add chapter, artifact, approval endpoints"
```

---

## Task 1.7: Cliente Supabase Storage / MinIO

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

- [ ] **Step 3: Adicionar storage settings ao `config.py`**

```python
storage_endpoint: str = "http://localhost:9000"
storage_access_key: str = "ebook"
storage_secret_key: str = "ebook-secret"
storage_bucket: str = "ebook-factory"
```

- [ ] **Step 4: Teste de smoke**

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

- [ ] **Step 5: Rodar teste (requer MinIO up)**

```bash
cd apps/backend && uv run pytest tests/test_storage.py -v
```

- [ ] **Step 6: Commit**

```bash
git add apps/backend/src/app/storage/ apps/backend/tests/test_storage.py apps/backend/pyproject.toml apps/backend/uv.lock
git commit -m "feat(backend): add S3-compatible storage client (MinIO/Supabase)"
```

---

## Task 1.8: Cliente Redis + health check de dependências

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
