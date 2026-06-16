import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps import get_db_session
from src.app.models import Chapter
from src.app.schemas import ChapterCreate, ChapterRead, ChapterUpdate

router = APIRouter(prefix="/chapters", tags=["chapters"])


@router.post("", response_model=ChapterRead, status_code=status.HTTP_201_CREATED)
async def create_chapter(
    payload: ChapterCreate, session: AsyncSession = Depends(get_db_session)
) -> Chapter:
    chapter = Chapter(
        project_id=payload.project_id,
        title=payload.title,
        order=payload.order,
    )
    session.add(chapter)
    await session.commit()
    await session.refresh(chapter)
    return chapter


@router.get("", response_model=list[ChapterRead])
async def list_chapters(
    project_id: uuid.UUID | None = None,
    session: AsyncSession = Depends(get_db_session),
) -> list[Chapter]:
    stmt = select(Chapter)
    if project_id:
        stmt = stmt.where(Chapter.project_id == project_id)
    result = await session.execute(stmt.order_by(Chapter.order))
    return list(result.scalars().all())


@router.patch("/{chapter_id}", response_model=ChapterRead)
async def update_chapter(
    chapter_id: uuid.UUID,
    payload: ChapterUpdate,
    session: AsyncSession = Depends(get_db_session),
) -> Chapter:
    chapter = await session.get(Chapter, chapter_id)
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    if payload.title is not None:
        chapter.title = payload.title
    if payload.content is not None:
        chapter.content = payload.content
    if payload.status is not None:
        chapter.status = payload.status
    if payload.version is not None:
        chapter.version = payload.version
    await session.commit()
    await session.refresh(chapter)
    return chapter
