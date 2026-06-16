from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.api.deps import get_db_session
from src.app.models import Approval
from src.app.schemas import ApprovalCreate, ApprovalRead

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.post("", response_model=ApprovalRead, status_code=status.HTTP_201_CREATED)
async def create_approval(
    payload: ApprovalCreate, session: AsyncSession = Depends(get_db_session)
) -> Approval:
    approval = Approval(
        artifact_id=payload.artifact_id,
        decision=payload.decision,
        feedback=payload.feedback,
    )
    session.add(approval)
    await session.commit()
    await session.refresh(approval)
    return approval
