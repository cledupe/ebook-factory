# Task 4: Frontend (Next.js + Shadcn UI)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 4 — Frontend
> **Tasks:** 4.1 a 4.5

---

## Task 4.1: Inicializar Next.js

**Files:**
- Create: `apps/frontend/` (via `pnpm create next-app`)

- [ ] **Step 1: Criar o app Next.js**

```bash
cd apps
pnpm create next-app@latest frontend --typescript --tailwind --app --no-src-dir --import-alias "@/*"
cd frontend
pnpm dlx shadcn@latest init
```

- [ ] **Step 2: Adicionar dependencias**

```bash
pnpm add zustand @tanstack/react-query react-hook-form zod @hookform/resolvers lucide-react
pnpm add -D @playwright/test
```

- [ ] **Step 3: Commit**

```bash
git add apps/frontend/
git commit -m "feat(frontend): initialize next.js with tailwind and shadcn ui"
```

---

## Task 4.2: Camada API client

**Files:**
- Create: `apps/frontend/lib/api/client.ts`
- Create: `apps/frontend/lib/api/projects.ts`
- Create: `apps/frontend/lib/api/workflows.ts`

Cliente `fetch` tipado usando `@ebook-factory/shared-types`. Hooks React Query para cada operacao.

- [ ] **Criar `lib/api/client.ts`**

```typescript
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}
```

- [ ] **Criar hooks para Projects e Workflows com React Query**

- [ ] **Commit**

```bash
git add apps/frontend/lib/api/
git commit -m "feat(frontend): add typed API client with react query hooks"
```

---

## Task 4.3: Telas principais

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/page.tsx` — lista + criar
- Create: `apps/frontend/app/(dashboard)/projects/[id]/page.tsx` — wizard
- Create: `apps/frontend/components/ideation-step.tsx`
- Create: `apps/frontend/components/outline-step.tsx`
- Create: `apps/frontend/components/chapter-step.tsx`
- Create: `apps/frontend/components/approval-dialog.tsx`
- Create: `apps/frontend/components/workflow-stepper.tsx`

`WorkflowStepper` mostra os 4 estagios (Ideacao, Estruturação, Escrita, Conversao) com indicador de progresso. Cada step tem: visualizacao do artefato, botoes "Aprovar", "Rejeitar", "Editar", "Regenerar" e campo de feedback.

- [ ] **Commit**

```bash
git add apps/frontend/app/ apps/frontend/components/
git commit -m "feat(frontend): add project wizard and workflow stepper ui"
```

---

## Task 4.4: Streaming de progresso

**Files:**
- Create: `apps/frontend/lib/api/sse.ts`
- Create: `apps/frontend/app/api/stream/[projectId]/route.ts` (proxy SSE)
- Modify: backend `apps/backend/src/app/api/workflows.py`

Backend emite eventos SSE por etapa (`workflow.started`, `workflow.node_entered`, `workflow.awaiting_approval`, `workflow.completed`). Frontend usa `EventSource` e atualiza UI em tempo real.

- [ ] **Commit**

```bash
git add apps/frontend/lib/api/sse.ts apps/frontend/app/api/stream/
git commit -m "feat(frontend): add SSE streaming for workflow progress"
```

---

## Task 4.5: Pagina de versoes e observabilidade

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/versions/page.tsx`
- Create: `apps/frontend/app/(dashboard)/projects/[id]/traces/page.tsx`

Listar historico de artefatos (com diff) e embed do Langfuse (link direto ao trace do projeto).

- [ ] **Commit**

```bash
git add apps/frontend/app/(dashboard)/projects/[id]/versions/ apps/frontend/app/(dashboard)/projects/[id]/traces/
git commit -m "feat(frontend): add version history and langfuse trace pages"
```
