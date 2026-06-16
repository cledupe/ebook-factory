import uuid

from src.app.models import (
    Approval,
    ApprovalDecision,
    Artifact,
    ArtifactType,
    Chapter,
    ChapterStatus,
    Project,
    ProjectStatus,
)


def test_create_project_in_memory():
    project = Project(title="Meu Ebook", status=ProjectStatus.IDEATION)
    assert project.id is None
    assert project.title == "Meu Ebook"
    assert project.status == ProjectStatus.IDEATION


def test_create_chapter_relationship():
    chapter = Chapter(
        project_id=uuid.uuid4(),
        title="Cap 1",
        status=ChapterStatus.PENDING,
        order=0,
        version=1,
    )
    assert chapter.version == 1
    assert chapter.status == ChapterStatus.PENDING


def test_create_artifact_with_content():
    artifact = Artifact(
        project_id=uuid.uuid4(),
        type=ArtifactType.IDEA,
        content={"title": "x", "subtitle": "y"},
    )
    assert artifact.content["title"] == "x"
    assert artifact.type == ArtifactType.IDEA


def test_create_approval_decision():
    approval = Approval(
        artifact_id=uuid.uuid4(),
        decision=ApprovalDecision.APPROVED,
        feedback="ok",
    )
    assert approval.decision == ApprovalDecision.APPROVED
