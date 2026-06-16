import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from src.app.db import engine
from src.app.db.base import Base
from src.app.main import app


@pytest_asyncio.fixture
async def client():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_create_chapter(client: AsyncClient):
    proj = await client.post("/projects", json={"title": "Proj"})
    pid = proj.json()["id"]

    response = await client.post(
        "/chapters",
        json={"project_id": pid, "title": "Cap 1", "order": 1},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Cap 1"
    assert data["version"] == 1

    response = await client.get(f"/chapters?project_id={pid}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    cid = data["id"]
    response = await client.patch(
        f"/chapters/{cid}",
        json={"content": "# Content", "status": "approved"},
    )
    assert response.status_code == 200
    assert response.json()["content"] == "# Content"
    assert response.json()["status"] == "approved"


@pytest.mark.asyncio
async def test_create_artifact_and_approval(client: AsyncClient):
    proj = await client.post("/projects", json={"title": "Proj"})
    pid = proj.json()["id"]

    art = await client.post(
        "/artifacts",
        json={"project_id": pid, "type": "idea", "content": {"title": "x"}},
    )
    assert art.status_code == 201
    aid = art.json()["id"]

    resp = await client.post(
        "/approvals",
        json={"artifact_id": aid, "decision": "approved", "feedback": "ok"},
    )
    assert resp.status_code == 201
    assert resp.json()["decision"] == "approved"
