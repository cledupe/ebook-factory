import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.app.models.enums import ArtifactType


class ArtifactCreate(BaseModel):
    project_id: uuid.UUID
    type: ArtifactType
    content: dict = {}


class ArtifactRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    project_id: uuid.UUID
    type: ArtifactType
    content: dict
    version: int
    created_at: datetime
