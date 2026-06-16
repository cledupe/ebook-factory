# Task 6: Observabilidade (Langfuse + OpenTelemetry + Prometheus)

> **Plano principal:** [`docs/superpowers/plans/2026-06-15-ebook-factory.md`](../plans/2026-06-15-ebook-factory.md)
> **Fase:** 6 — Observabilidade
> **Tasks:** 6.1 a 6.4

---

## Task 6.1: OpenTelemetry no backend

**Files:**
- Create: `apps/backend/src/app/observability/__init__.py`
- Create: `apps/backend/src/app/observability/otel.py`
- Modify: `apps/backend/src/app/main.py`

- [ ] **Step 1: Configurar tracer OTLP**

Exportar para coletor OTLP (ou stdout em dev). Instrumentar FastAPI + SQLAlchemy + Redis.

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def setup_tracing(service_name: str = "ebook-factory-backend") -> None:
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )
    trace.set_tracer_provider(provider)
```

- [ ] **Step 2: Chamar `setup_tracing()` no `lifespan` do FastAPI**

- [ ] **Commit**

```bash
git add apps/backend/src/app/observability/ apps/backend/src/app/main.py
git commit -m "feat(observability): add opentelemetry tracing with otlp export"
```

---

## Task 6.2: Prometheus metrics

**Files:**
- Create: `apps/backend/src/app/observability/metrics.py`
- Modify: `apps/backend/src/app/main.py`

- [ ] **Step 1: Criar metricas custom**

```python
from prometheus_client import Counter, Histogram, generate_latest

workflow_stage_duration = Histogram(
    "workflow_stage_duration_seconds",
    "Duration per workflow stage",
    ["stage"],
)
workflow_approvals = Counter(
    "workflow_approvals_total",
    "Total approval decisions",
    ["decision"],
)
llm_tokens = Counter(
    "llm_tokens_total",
    "Total LLM tokens consumed",
    ["agent", "model"],
)
llm_cost = Counter(
    "llm_cost_usd_total",
    "Total LLM cost in USD",
    ["agent", "model"],
)
```

- [ ] **Step 2: Adicionar endpoint `GET /metrics`**

```python
from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter(tags=["metrics"])


@router.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

- [ ] **Commit**

```bash
git add apps/backend/src/app/observability/metrics.py apps/backend/src/app/main.py
git commit -m "feat(observability): add prometheus metrics and /metrics endpoint"
```

---

## Task 6.3: Langfuse self-hosted

**Files:**
- Modify: `infra/docker-compose.yml`

- [ ] **Validar dashboard**

Ja incluído na infra/task 0.2. Acessar `http://localhost:3001` e configurar DSN nos agentes (LangfuseCallbackHandler ja configurado na Task 3.1).

- [ ] **Commit** (se houver ajustes)

```bash
git add infra/docker-compose.yml
git commit -m "chore(infra): adjust langfuse service configuration"
```

---

## Task 6.4: Grafana + dashboards

**Files:**
- Create: `infra/grafana/dashboards/workflow.json`
- Create: `infra/grafana/dashboards/llm-costs.json`
- Create: `infra/grafana/datasources/prometheus.yml`
- Modify: `infra/docker-compose.yml`

- [ ] **Step 1: Adicionar servico grafana ao compose**

```yaml
grafana:
  image: grafana/grafana:latest
  container_name: ef-grafana
  ports:
    - "3002:3000"
  volumes:
    - grafana_data:/var/lib/grafana
    - ./grafana/datasources:/etc/grafana/provisioning/datasources
    - ./grafana/dashboards:/etc/grafana/provisioning/dashboards
  environment:
    GF_AUTH_ANONYMOUS_ENABLISHED: "true"
  depends_on:
    - prometheus
```

- [ ] **Step 2: Provisionsr Prometheus datasource e dashboards basicos**

Duracao por estagio, taxa de aprovacao, custo por agente, tokens por minuto.

- [ ] **Commit**

```bash
git add infra/grafana/ infra/docker-compose.yml
git commit -m "feat(observability): add grafana with provisioned dashboards"
```
