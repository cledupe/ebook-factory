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
async def test_create_list_get_update_delete_project(client: AsyncClient):
    response = await client.post("/projects", json={"title": "Meu Ebook"})
    assert response.status_code == 201
    data = response.json()
    pid = data["id"]
    assert data["title"] == "Meu Ebook"
    assert data["status"] == "ideation"

    response = await client.get("/projects")
    assert response.status_code == 200
    assert any(p["id"] == pid for p in response.json())

    response = await client.get(f"/projects/{pid}")
    assert response.status_code == 200

    response = await client.patch(f"/projects/{pid}", json={"title": "Novo"})
    assert response.status_code == 200
    assert response.json()["title"] == "Novo"

    response = await client.delete(f"/projects/{pid}")
    assert response.status_code == 204

    response = await client.get(f"/projects/{pid}")
    assert response.status_code == 404
