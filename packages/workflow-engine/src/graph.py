from langgraph.graph import StateGraph, START

from src.state import WorkflowState


def idea_node(state: WorkflowState) -> dict:
    return {"current_stage": "ideation_awaiting_approval"}


def outline_node(state: WorkflowState) -> dict:
    return {"current_stage": "outline_awaiting_approval"}


def write_chapter_node(state: WorkflowState) -> dict:
    return {"current_stage": "writing_awaiting_approval"}


def reflect_node(state: WorkflowState) -> dict:
    return {"current_stage": "reflection_done"}


def convert_node(state: WorkflowState) -> dict:
    return {"current_stage": "completed"}


def create_graph() -> StateGraph:
    builder = StateGraph(WorkflowState)
    builder.add_node("idea", idea_node)
    builder.add_node("outline", outline_node)
    builder.add_node("write_chapter", write_chapter_node)
    builder.add_node("reflect", reflect_node)
    builder.add_node("convert", convert_node)
    builder.add_edge(START, "idea")
    builder.add_conditional_edges(
        "idea",
        lambda s: "outline" if s.idea else "idea",
    )
    builder.add_conditional_edges(
        "outline",
        lambda s: "write_chapter" if s.outline else "outline",
    )
    builder.add_edge("write_chapter", "reflect")
    builder.add_conditional_edges(
        "reflect",
        lambda s: "write_chapter" if s.iterations > 0 else "convert",
    )
    builder.add_edge("convert", "reflect")
    return builder.compile()
