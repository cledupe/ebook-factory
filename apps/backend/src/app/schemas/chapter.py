import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.app.models.enums import ChapterStatus


class ChapterCreate(BaseModel):
    project_id: uuid.UUID
    title: str = Field(min_length=1, max_length=255)
    order: int = 0


class ChapterUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    content: str | None = None
    status: ChapterStatus | None = None
    version: int | None = None


class ChapterRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    title: str
    content: str | None
    order: int
    version: int
    status: ChapterStatus
    created_at: datetime
    updated_at: datetime
