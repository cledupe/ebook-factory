import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.state import WorkflowState


def test_workflow_state_defaults():
    state = WorkflowState(project_id="abc-123")
    assert state.project_id == "abc-123"
    assert state.current_stage == "ideation"
    assert state.idea is None
    assert state.chapters == {}
    assert state.reflection_notes == []
    assert state.iterations == 0


def test_workflow_state_with_idea():
    state = WorkflowState(
        project_id="abc-123",
        current_stage="structuring",
        idea={"title": "Meu Livro", "subtitle": "Guia Prático"},
        iterations=1,
    )
    assert state.idea["title"] == "Meu Livro"
    assert state.current_stage == "structuring"
    assert state.iterations == 1
