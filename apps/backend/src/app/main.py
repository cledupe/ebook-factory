from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.app.api import approvals, artifacts, chapters, health, projects


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Ebook Factory API", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(projects.router)
    app.include_router(chapters.router)
    app.include_router(artifacts.router)
    app.include_router(approvals.router)
    return app


app = create_app()
