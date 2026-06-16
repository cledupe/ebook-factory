from fastapi import APIRouter, status
from sqlalchemy import text

from src.app.db import engine
from src.app.redis_client import get_redis

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
