import uuid

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter(prefix="/workflows", tags=["workflows"])


class ResumeRequest(BaseModel):
    decision: str
    feedback: str | None = None


@router.post("/{project_id}/start")
async def start_workflow(project_id: uuid.UUID):
    # TODO: integrar com langgraph
    return {"project_id": str(project_id), "status": "started"}


@router.post("/{project_id}/resume")
async def resume_workflow(project_id: uuid.UUID, body: ResumeRequest):
    # TODO: chamar resume_workflow() do workflow-engine
    return {
        "project_id": str(project_id),
        "decision": body.decision,
        "feedback": body.feedback,
    }


@router.get("/{project_id}/state")
async def get_workflow_state(project_id: uuid.UUID):
    # TODO: buscar checkpoint atual
    return {
        "project_id": str(project_id),
        "current_stage": "ideation_awaiting_approval",
        "pending_artifact_id": None,
    }
