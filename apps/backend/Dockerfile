ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /app

RUN pip install uv==0.6.0

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-editable

COPY src/ src/
RUN uv sync --frozen --no-dev --no-editable

FROM python:${PYTHON_VERSION}-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv .venv
COPY --from=builder /app/src src/
COPY migrations/ migrations/
COPY alembic.ini alembic.ini

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:${PYTHONPATH}" \
    APP_ENV=production

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn --factory src.app.main:create_app --host 0.0.0.0 --port 8000 --workers 4"]
