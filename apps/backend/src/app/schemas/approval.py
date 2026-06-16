import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.app.models.enums import ApprovalDecision


class ApprovalCreate(BaseModel):
    artifact_id: uuid.UUID
    decision: ApprovalDecision
    feedback: str | None = None


class ApprovalRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    artifact_id: uuid.UUID
    decision: ApprovalDecision
    feedback: str | None
    created_at: datetime
