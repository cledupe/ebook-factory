import pytest

from src.app.redis_client import get_redis


@pytest.mark.asyncio
async def test_redis_client_init():
    redis = get_redis()
    assert redis is not None


@pytest.mark.asyncio
async def test_redis_ping_skipped_if_unavailable():
    redis = get_redis()
    try:
        result = await redis.ping()
        assert result is True
    except Exception:
        pytest.skip("Redis not available")
