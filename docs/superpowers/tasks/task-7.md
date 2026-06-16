# Task 7: Polimento MVP

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 7 — Polimento MVP
> **Tasks:** 7.1 a 7.6

---

## Task 7.1: Autenticacao com OTP + Supabase Auth

**Files:**
- Modify: `apps/backend/src/app/api/deps.py`
- Create: `apps/backend/src/app/auth/jwt.py`
- Create: `apps/backend/src/app/auth/otp.py`
- Create: `apps/frontend/lib/auth/supabase.ts`
- Create: `apps/frontend/middleware.ts`

- [ ] **Implementar JWT verification no backend**

```python
# apps/backend/src/app/auth/jwt.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # TODO: verificar JWT contra Supabase Auth
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"user_id": "placeholder"}
```

- [ ] **Adicionar `user_id` em Project e RLS policies no Postgres**

- [ ] **Configurar session no frontend com Supabase client**

- [ ] **Criar servico OTP em `src/app/auth/otp.py`**

```python
# apps/backend/src/app/auth/otp.py
import secrets
from datetime import datetime, timedelta

from apps.backend.src.app.redis_client import get_redis


OTP_PREFIX = "otp:"
OTP_EXPIRY_SECONDS = 300  # 5 minutos
OTP_LENGTH = 6


def _otp_key(user_id: str, action: str) -> str:
    return f"{OTP_PREFIX}{user_id}:{action}"


async def generate_otp(user_id: str, action: str) -> str:
    redis = get_redis()
    code = "".join(secrets.choice("0123456789") for _ in range(OTP_LENGTH))
    await redis.setex(_otp_key(user_id, action), OTP_EXPIRY_SECONDS, code)
    return code


async def verify_otp(user_id: str, action: str, code: str) -> bool:
    redis = get_redis()
    stored = await redis.get(_otp_key(user_id, action))
    if stored is None or stored != code:
        return False
    await redis.delete(_otp_key(user_id, action))
    return True
```

- [ ] **Criar decorator/dependency `require_otp` em `src/app/auth/otp.py`**

```python
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel


class OTPRequest(BaseModel):
    otp_code: str


async def require_otp(
    user_id: str = Depends(verify_token),
    otp: OTPRequest = ...,
    action: str = ...,
) -> str:
    valid = await verify_otp(user_id["user_id"], action, otp.otp_code)
    if not valid:
        raise HTTPException(status_code=403, detail="Invalid or expired OTP")
    return user_id["user_id"]
```

- [ ] **Aplicar `require_otp` nos endpoints criticos**

Endpoints que exigem OTP: aprovar artefato (`POST /approvals`), iniciar conversao (`POST /exports/{id}`), deletar projeto (`DELETE /projects/{id}`).

```python
# Exemplo de uso em approvals.py
from apps.backend.src.app.auth.otp import require_otp, OTPRequest


@router.post("/approvals")
async def create_approval(
    payload: ApprovalCreate,
    session: SessionDep,
    user: str = Depends(lambda: require_otp(action="approve_artifact")),
):
    ...
```

- [ ] **Endpoints para gerar e validar OTP**

```python
# apps/backend/src/app/auth/otp.py (adicionar router)
from fastapi import APIRouter

otp_router = APIRouter(prefix="/auth/otp", tags=["auth"])


@otp_router.post("/send")
async def send_otp(action: str, user: str = Depends(verify_token)):
    code = await generate_otp(user["user_id"], action)
    # TODO: enviar por email (em dev, retornar no response)
    return {"message": "OTP sent", "expires_in": OTP_EXPIRY_SECONDS}
```

- [ ] **Commit**

```bash
git add apps/backend/src/app/auth/ apps/backend/src/app/api/deps.py apps/frontend/lib/auth/ apps/frontend/middleware.ts
git commit -m "feat(auth): add supabase auth with OTP authorization for critical actions"
```

---

## Task 7.2: Tratamento de erros global

**Files:**
- Modify: `apps/backend/src/app/main.py`
- Create: `apps/backend/src/app/api/errors.py`

- [ ] **Criar handler global**

```python
# apps/backend/src/app/api/errors.py
from fastapi import Request
from fastapi.responses import JSONResponse


async def global_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "internal_error", "message": str(exc), "details": None}},
    )
```

- [ ] **Registrar middleware no main.py**

- [ ] **Commit**

```bash
git add apps/backend/src/app/api/errors.py apps/backend/src/app/main.py
git commit -m "feat(backend): add global error handler for consistent error format"
```

---

## Task 7.3: Versionamento UI

**Files:**
- Modify: `apps/frontend/components/artifact-viewer.tsx`
- Create: `apps/frontend/components/version-diff.tsx`

- [ ] **Mostrar lista de versoes por artefato**

- [ ] **Implementar diff side-by-side entre versoes**

- [ ] **Commit**

```bash
git add apps/frontend/components/artifact-viewer.tsx apps/frontend/components/version-diff.tsx
git commit -m "feat(frontend): add version diff viewer for artifacts"
```

---

## Task 7.4: Cost tracking UI

**Files:**
- Create: `apps/frontend/app/(dashboard)/projects/[id]/costs/page.tsx`
- Create: `apps/backend/src/app/api/metrics.py`

- [ ] **Endpoint `GET /projects/{id}/costs`**

Retorna breakdown por agente/modelo/etapa.

- [ ] **Frontend renderiza graficos (Recharts ou Tremor)**

- [ ] **Commit**

```bash
git add apps/backend/src/app/api/metrics.py apps/frontend/
git commit -m "feat(costs): add cost tracking endpoint and chart UI"
```

---

## Task 7.5: Testes E2E (Playwright)

**Files:**
- Create: `apps/frontend/e2e/full-workflow.spec.ts`
- Create: `apps/frontend/playwright.config.ts`

- [ ] **Criar config do Playwright**

- [ ] **Cenario E2E:** criar projeto, rodar ideacao, aprovar, rodar outline, editar capitulo, aprovar, exportar EPUB, validar download.

- [ ] **Commit**

```bash
git add apps/frontend/e2e/ apps/frontend/playwright.config.ts
git commit -m "test(e2e): add playwright e2e test for full workflow"
```

---

## Task 7.6: Documentacao e deploy

**Files:**
- Create: `docs/architecture.md`
- Create: `docs/development.md`
- Create: `docs/deployment.md`
- Create: `infra/prod/docker-compose.yml`
- Create: `infra/prod/caddy/Caddyfile`

- [ ] **Docs de arquitetura, setup local e deploy**

- [ ] **Docker Compose de producao com Caddy reverse proxy + TLS**

- [ ] **Commit**

```bash
git add docs/ infra/prod/
git commit -m "docs: add architecture, development, and deployment guides"
```
