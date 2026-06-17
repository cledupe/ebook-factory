from pydantic import BaseModel, Field


class WorkflowState(BaseModel):
    project_id: str
    current_stage: str = "ideation"
    idea: dict | None = None
    outline: dict | None = None
    chapters: dict[int, str] = Field(default_factory=dict)
    pending_artifact_id: str | None = None
    reflection_notes: list[str] = Field(default_factory=list)
    iterations: int = 0
    error: str | None = None
