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
