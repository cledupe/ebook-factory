# Task 3: AI Agents (Ideação, Estruturação, Escrita, Reflexão)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 3 — AI Agents
> **Tasks:** 3.1 a 3.7

---

## Task 3.1: Cliente LLM com Langfuse

**Files:**
- Create: `packages/ai-agents/src/llm.py`
- Create: `packages/ai-agents/pyproject.toml`

- [ ] **Step 1: Criar `pyproject.toml`**

```toml
[project]
name = "ebook-factory-ai-agents"
version = "0.1.0"
description = "LLM agents for ebook generation"
requires-python = ">=3.12"
dependencies = [
    "langchain>=0.3.0",
    "langchain-openai>=0.2.0",
    "langfuse>=2.50.0",
    "pydantic>=2.9.0",
]

[tool.uv]
dev-dependencies = ["pytest>=8.3.0", "ruff>=0.6.0"]
```

- [ ] **Step 2: Criar `src/llm.py`**

Wrapper sobre `langchain.chat_models.ChatOpenAI` que:
- Adiciona callback `LangfuseCallbackHandler`
- Registra tokens, custo e latência em cada chamada
- Expõe `invoke_with_trace(prompt, **kwargs)` retornando `LLMResult`

```python
from functools import lru_cache

from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler

from ebook_factory_ai_agents.src.config import get_settings


@lru_cache
def get_langfuse_handler() -> CallbackHandler:
    settings = get_settings()
    return CallbackHandler(
        public_key=settings.langfuse_public_key,
        secret_key=settings.langfuse_secret_key,
        host=settings.langfuse_host,
    )


@lru_cache
def get_llm(model: str | None = None) -> ChatOpenAI:
    settings = get_settings()
    return ChatOpenAI(
        model=model or settings.llm_model,
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        callbacks=[get_langfuse_handler()],
    )
```

- [ ] **Step 3: Commit**

```bash
git add packages/ai-agents/
git commit -m "feat(agents): add LLM client with langfuse tracing"
```

---

## Task 3.2: Idea Agent

**Files:**
- Create: `packages/ai-agents/src/agents/__init__.py`
- Create: `packages/ai-agents/src/agents/idea.py`
- Create: `packages/ai-agents/src/prompts/idea.py`
- Create: `packages/ai-agents/tests/test_idea_agent.py`

Schema de saída (Pydantic): `IdeaArtifact(title, subtitle, persona, problem, promise, outline_preview)`.

- [ ] **Criar `src/agents/idea.py`**

```python
from pydantic import BaseModel, Field

from ebook_factory_ai_agents.src.llm import get_llm
from ebook_factory_ai_agents.src.prompts.idea import IDEA_SYSTEM_PROMPT


class IdeaArtifact(BaseModel):
    title: str
    subtitle: str
    persona: str
    problem: str
    promise: str
    outline_preview: list[str]


class IdeaAgent:
    def __init__(self, model: str | None = None):
        self.llm = get_llm(model).with_structured_output(IdeaArtifact)

    def generate(self, niche: str, theme: str, audience: str | None = None) -> IdeaArtifact:
        prompt = IDEA_SYSTEM_PROMPT.format(
            niche=niche, theme=theme, audience=audience or "general"
        )
        return self.llm.invoke(prompt)
```

- [ ] **Teste com LLM fake (`FakeChatModel`) validando que o prompt é montado e o JSON parseado.**

- [ ] **Commit**

```bash
git add packages/ai-agents/src/agents/idea.py
git commit -m "feat(agents): add idea agent with structured output"
```

---

## Task 3.3: Outline Agent

**Files:**
- Create: `packages/ai-agents/src/agents/outline.py`
- Create: `packages/ai-agents/src/prompts/outline.py`
- Create: `packages/ai-agents/tests/test_outline_agent.py`

Schema: `OutlineArtifact(introduction, chapters: list[ChapterSpec], conclusion)`. Cada `ChapterSpec`: `order, title, objectives: list[str], topics: list[str]`.

- [ ] **Commit**

```bash
git add packages/ai-agents/src/agents/outline.py
git commit -m "feat(agents): add outline agent with chapter specs"
```

---

## Task 3.4: Writer Agent

**Files:**
- Create: `packages/ai-agents/src/agents/writer.py`
- Create: `packages/ai-agents/src/prompts/writer.py`
- Create: `packages/ai-agents/tests/test_writer_agent.py`

Schema: `ChapterContent(chapter_id, markdown_content, word_count)`. Recebe `outline` e gera um capítulo por chamada. Teste valida que `markdown_content` é gerado e contém o título.

- [ ] **Commit**

```bash
git add packages/ai-agents/src/agents/writer.py
git commit -m "feat(agents): add writer agent for chapter generation"
```

---

## Task 3.5: Reflection Agent

**Files:**
- Create: `packages/ai-agents/src/agents/reflection.py`
- Create: `packages/ai-agents/src/prompts/reflection.py`
- Create: `packages/ai-agents/tests/test_reflection_agent.py`

Schema: `ReflectionResult(issues: list[str], suggestions: list[str], score: float)`. Nao altera o artefato original — so retorna criticas.

- [ ] **Commit**

```bash
git add packages/ai-agents/src/agents/reflection.py
git commit -m "feat(agents): add reflection agent for content critique"
```

---

## Task 3.6: Loop de reflexao

**Files:**
- Create: `packages/ai-agents/src/agents/loop.py`

Funcao `reflect_and_improve(artifact, max_iterations=2, score_threshold=0.8)` que executa Reflection + regeneracao do agente original enquanto `score < threshold` e `iteration < max_iterations`. Persiste cada iteracao como Artifact `type=reflection`.

- [ ] **Commit**

```bash
git add packages/ai-agents/src/agents/loop.py
git commit -m "feat(agents): add reflect-and-improve loop with iteration limit"
```

---

## Task 3.7: Integracao com workflow

**Files:**
- Modify: `packages/workflow-engine/src/nodes/idea.py`
- Modify: `packages/workflow-engine/src/nodes/outline.py`
- Modify: `packages/workflow-engine/src/nodes/write_chapter.py`
- Modify: `packages/workflow-engine/src/nodes/reflect.py`

Substituir implementacoes stub pelos agentes reais. Cada no deve:
1. Criar Artifact inicial
2. Rodar `reflect_and_improve`
3. Persistir versao final + cria `pending_artifact_id` para HITL

- [ ] **Commit**

```bash
git add packages/workflow-engine/src/nodes/
git commit -m "feat(workflow): integrate AI agents into workflow nodes"
```
