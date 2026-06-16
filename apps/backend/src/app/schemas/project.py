import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from src.app.models.enums import ProjectStatus


class ProjectBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    status: ProjectStatus | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
