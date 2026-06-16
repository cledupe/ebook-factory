# Task 5: Conversao (Pandoc -> EPUB/PDF/DOCX)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 5 — Conversao
> **Tasks:** 5.1 a 5.4

---

## Task 5.1: Servico de conversao

**Files:**
- Create: `packages/kdp-converter/pyproject.toml`
- Create: `packages/kdp-converter/src/converter.py`
- Create: `packages/kdp-converter/src/templates/book.md.j2`
- Create: `packages/kdp-converter/src/templates/epub-metadata.xml`
- Create: `packages/kdp-converter/tests/test_converter.py`

Funcao `convert_book(project_id, formats: list[str])` que:
1. Carrega capitulos aprovados do banco
2. Renderiza Jinja -> Markdown unificado
3. Executa Pandoc para cada formato solicitado
4. Faz upload para Supabase Storage em `projects/{id}/exports/`
5. Retorna URLs pre-assinadas

- [ ] **Criar `pyproject.toml`**

```toml
[project]
name = "ebook-factory-kdp-converter"
version = "0.1.0"
description = "Pandoc EPUB/PDF/DOCX conversion"
requires-python = ">=3.12"
dependencies = [
    "jinja2>=3.1.0",
    "pandoc>=2.4",
    "boto3>=1.35.0",
]

[tool.uv]
dev-dependencies = ["pytest>=8.3.0", "ruff>=0.6.0"]
```

- [ ] **Criar `src/converter.py` com logica de conversao**

- [ ] **Commit**

```bash
git add packages/kdp-converter/
git commit -m "feat(converter): add pandoc conversion service with jinja templates"
```

---

## Task 5.2: Endpoint de exportacao

**Files:**
- Create: `apps/backend/src/app/api/exports.py`
- Modify: `apps/backend/src/app/main.py`

`POST /exports/{project_id}` com body `{"formats": ["epub", "pdf", "docx"]}`. Retorna job ID. Worker assincrono processa e atualiza status.

- [ ] **Commit**

```bash
git add apps/backend/src/app/api/exports.py apps/backend/src/app/main.py
git commit -m "feat(backend): add export endpoint for kdp conversion"
```

---

## Task 5.3: Worker assincrono

**Files:**
- Create: `apps/backend/src/app/workers/__init__.py`
- Create: `apps/backend/src/app/workers/exports.py`
- Create: `apps/backend/src/app/workers/runner.py`

Usar `arq` (Redis-based) ou `taskiq` para processar jobs. `runner.py` inicia worker junto com FastAPI em dev ou standalone em prod.

- [ ] **Commit**

```bash
git add apps/backend/src/app/workers/
git commit -m "feat(backend): add async worker for export jobs"
```

---

## Task 5.4: Download no frontend

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/export/page.tsx`
- Create: `apps/frontend/components/export-panel.tsx`

Botoes para EPUB/PDF/DOCX com polling de status e links de download.

- [ ] **Commit**

```bash
git add apps/frontend/
git commit -m "feat(frontend): add export page with download buttons"
```
