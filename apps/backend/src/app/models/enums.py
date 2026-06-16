from enum import StrEnum


class ProjectStatus(StrEnum):
    IDEATION = "ideation"
    STRUCTURING = "structuring"
    WRITING = "writing"
    REVIEW = "review"
    CONVERTING = "converting"
    COMPLETED = "completed"
    FAILED = "failed"


class ChapterStatus(StrEnum):
    PENDING = "pending"
    GENERATING = "generating"
    GENERATED = "generated"
    APPROVED = "approved"
    REJECTED = "rejected"


class ArtifactType(StrEnum):
    IDEA = "idea"
    OUTLINE = "outline"
    CHAPTER = "chapter"
    REFLECTION = "reflection"


class ApprovalDecision(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    EDITED = "edited"
    REGENERATE = "regenerate"
