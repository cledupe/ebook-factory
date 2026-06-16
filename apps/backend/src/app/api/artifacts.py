import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps import get_db_session
from src.app.models import Artifact
from src.app.models.enums import ArtifactType
from src.app.schemas import ArtifactCreate, ArtifactRead

router = APIRouter(prefix="/artifacts", tags=["artifacts"])


@router.post("", response_model=ArtifactRead, status_code=status.HTTP_201_CREATED)
async def create_artifact(
    payload: ArtifactCreate, session: AsyncSession = Depends(get_db_session)
) -> Artifact:
    artifact = Artifact(
        project_id=payload.project_id,
        type=payload.type,
        content=payload.content,
    )
    session.add(artifact)
    await session.commit()
    await session.refresh(artifact)
    return artifact


@router.get("", response_model=list[ArtifactRead])
async def list_artifacts(
    project_id: uuid.UUID | None = None,
    type: ArtifactType | None = None,
    session: AsyncSession = Depends(get_db_session),
) -> list[Artifact]:
    stmt = select(Artifact)
    if project_id:
        stmt = stmt.where(Artifact.project_id == project_id)
    if type:
        stmt = stmt.where(Artifact.type == type)
    result = await session.execute(stmt.order_by(Artifact.created_at.desc()))
    return list(result.scalars().all())
