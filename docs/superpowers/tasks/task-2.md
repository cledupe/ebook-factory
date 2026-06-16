# Task 2: Workflow Engine (LangGraph + Human-in-the-Loop)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 2 — Workflow Engine
> **Tasks:** 2.1 a 2.5

---

## Task 2.1: Definir estado do workflow

**Files:**
- Create: `packages/workflow-engine/src/state.py`
- Create: `packages/workflow-engine/src/__init__.py`
- Create: `packages/workflow-engine/pyproject.toml`
- Create: `packages/workflow-engine/tests/test_state.py`

- [ ] **Step 1: Criar `pyproject.toml` do package**

```toml
[project]
name = "ebook-factory-workflow-engine"
version = "0.1.0"
description = "LangGraph state machine with HITL"
requires-python = ">=3.12"
dependencies = [
    "langgraph>=0.2.0",
    "pydantic>=2.9.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=8.3.0",
    "ruff>=0.6.0",
]
```

- [ ] **Step 2: Criar `src/state.py`**

```python
from pydantic import BaseModel, Field


class WorkflowState(BaseModel):
    project_id: str
    current_stage: str = "ideation"
    idea: dict | None = None
    outline: dict | None = None
    chapters: dict[int, str] = Field(default_factory=dict)
    pending_artifact_id: str | None = None
    reflection_notes: list[str] = Field(default_factory=list)
    iterations: int = 0
    error: str | None = None
```

- [ ] **Step 3: Criar `src/__init__.py`**

```python
from packages.workflow_engine.src.state import WorkflowState

__all__ = ["WorkflowState"]
```

- [ ] **Step 4: Criar `tests/test_state.py`**

```python
from packages.workflow_engine.src.state import WorkflowState


def test_workflow_state_defaults():
    state = WorkflowState(project_id="abc-123")
    assert state.project_id == "abc-123"
    assert state.current_stage == "ideation"
    assert state.idea is None
    assert state.chapters == {}
    assert state.reflection_notes == []
    assert state.iterations == 0


def test_workflow_state_with_idea():
    state = WorkflowState(
        project_id="abc-123",
        current_stage="structuring",
        idea={"title": "Meu Livro", "subtitle": "Guia Prático"},
        iterations=1,
    )
    assert state.idea["title"] == "Meu Livro"
    assert state.current_stage == "structuring"
    assert state.iterations == 1
```

- [ ] **Step 5: Rodar testes**

```bash
cd packages/workflow-engine && uv run pytest -v
```

Expected: 2 passed.

- [ ] **Step 6: Commit**

```bash
git add packages/workflow-engine/
git commit -m "feat(workflow): add typed workflow state (Pydantic)"
```

---

## Task 2.2: Grafo base (transições)

**Files:**
- Create: `packages/workflow-engine/src/graph.py`
- Create: `packages/workflow-engine/src/nodes/__init__.py`

- [ ] **Step 1: Criar `src/graph.py`**

```python
from langgraph.graph import StateGraph, START

from packages.workflow_engine.src.state import WorkflowState


def idea_node(state: WorkflowState) -> dict:
    return {"current_stage": "ideation_awaiting_approval"}


def outline_node(state: WorkflowState) -> dict:
    return {"current_stage": "outline_awaiting_approval"}


def write_chapter_node(state: WorkflowState) -> dict:
    return {"current_stage": "writing_awaiting_approval"}


def reflect_node(state: WorkflowState) -> dict:
    return {"current_stage": "reflection_done"}


def convert_node(state: WorkflowState) -> dict:
    return {"current_stage": "completed"}


def create_graph() -> StateGraph:
    builder = StateGraph(WorkflowState)
    builder.add_node("idea", idea_node)
    builder.add_node("outline", outline_node)
    builder.add_node("write_chapter", write_chapter_node)
    builder.add_node("reflect", reflect_node)
    builder.add_node("convert", convert_node)
    builder.add_edge(START, "idea")
    builder.add_conditional_edges(
        "idea",
        lambda s: "outline" if s.idea else "idea",
    )
    builder.add_conditional_edges(
        "outline",
        lambda s: "write_chapter" if s.outline else "outline",
    )
    builder.add_edge("write_chapter", "reflect")
    builder.add_conditional_edges(
        "reflect",
        lambda s: "write_chapter" if s.iterations > 0 else "convert",
    )
    builder.add_edge("convert", "reflect")
    return builder.compile()
```

- [ ] **Step 2: Criar `src/nodes/__init__.py`**

```python
```

- [ ] **Step 3: Commit**

```bash
git add packages/workflow-engine/src/graph.py packages/workflow-engine/src/nodes/
git commit -m "feat(workflow): add base state graph with transitions"
```

---

## Task 2.3: Persistência (checkpoints)

**Files:**
- Create: `packages/workflow-engine/src/checkpoint.py`

- [ ] **Step 1: Criar `src/checkpoint.py`**

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.checkpoint.postgres import PostgresSaver


def create_sqlite_checkpointer(db_path: str = "checkpoints.db") -> SqliteSaver:
    return SqliteSaver.from_conn_string(db_path)


def create_postgres_checkpointer(connection_string: str) -> PostgresSaver:
    return PostgresSaver.from_conn_string(connection_string)
```

- [ ] **Step 2: Commit**

```bash
git add packages/workflow-engine/src/checkpoint.py
git commit -m "feat(workflow): add checkpoint persistence (sqlite/postgres)"
```

---

## Task 2.4: Resume após aprovação

**Files:**
- Create: `packages/workflow-engine/src/resume.py`

- [ ] **Step 1: Criar `src/resume.py`**

```python
from langgraph.graph.graph import CompiledGraph, StateGraph

from packages.workflow_engine.src.state import WorkflowState


def resume_workflow(
    graph: CompiledGraph,
    thread_id: str,
    decision: str,
    feedback: str | None = None,
) -> dict:
    config = {"configurable": {"thread_id": thread_id}}

    if decision == "approved":
        return graph.invoke(None, config)
    elif decision == "rejected":
        state = graph.get_state(config).values
        state["current_stage"] = "rejected"
        return state
    elif decision == "edited":
        return graph.invoke(None, config)
    elif decision == "regenerate":
        state = graph.get_state(config).values
        state["iterations"] += 1
        return graph.invoke(None, config)

    raise ValueError(f"Unknown decision: {decision}")
```

- [ ] **Step 2: Commit**

```bash
git add packages/workflow-engine/src/resume.py
git commit -m "feat(workflow): add resume logic after human approval"
```

---

## Task 2.5: Endpoints do workflow no backend

**Files:**
- Create: `apps/backend/src/app/api/workflows.py`
- Modify: `apps/backend/src/app/main.py`

- [ ] **Step 1: Criar `src/app/api/workflows.py`**

```python
import uuid

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/workflows", tags=["workflows"])


class ResumeRequest(BaseModel):
    decision: str
    feedback: str | None = None


@router.post("/{project_id}/start")
async def start_workflow(project_id: uuid.UUID):
    # TODO: integrar com langgraph
    return {"project_id": str(project_id), "status": "started"}


@router.post("/{project_id}/resume")
async def resume_workflow(project_id: uuid.UUID, body: ResumeRequest):
    # TODO: chamar resume_workflow() do workflow-engine
    return {
        "project_id": str(project_id),
        "decision": body.decision,
        "feedback": body.feedback,
    }


@router.get("/{project_id}/state")
async def get_workflow_state(project_id: uuid.UUID):
    # TODO: buscar checkpoint atual
    return {
        "project_id": str(project_id),
        "current_stage": "ideation_awaiting_approval",
        "pending_artifact_id": None,
    }
```

- [ ] **Step 2: Registrar router em `main.py`**

```python
from apps.backend.src.app.api import health, projects, workflows

app.include_router(workflows.router)
```

- [ ] **Step 3: Commit**

```bash
git add apps/backend/src/app/api/workflows.py apps/backend/src/app/main.py
git commit -m "feat(backend): add workflow endpoints (start, resume, state)"
```
