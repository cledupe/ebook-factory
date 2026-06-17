from langgraph.graph.graph import CompiledGraph, StateGraph

from src.state import WorkflowState


def resume_workflow(
    graph: CompiledGraph,
    thread_id: str,
    decision: str,
    feedback: str | None = None,
) -> dict:
    config = {"configurable": {"thread_id": thread_id}}

    if decision == "approved":
        return graph.invoke(None, config)
    elif decision == "rejected":
        state = graph.get_state(config).values
        state["current_stage"] = "rejected"
        return state
    elif decision == "edited":
        return graph.invoke(None, config)
    elif decision == "regenerate":
        state = graph.get_state(config).values
        state["iterations"] += 1
        return graph.invoke(None, config)

    raise ValueError(f"Unknown decision: {decision}")
