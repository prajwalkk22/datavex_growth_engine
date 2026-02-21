from langgraph.graph import StateGraph
from app.state import PipelineState
from app.agents.signal_discovery import discover_signals
from app.agents.signal_scoring import score_signal
from app.agents.signal_validator import validate_signal
from app.agents.serp_gap import serp_gap_analysis

def build_graph():
    graph = StateGraph(PipelineState)

    def discover(state):
        state["raw_signals"] = discover_signals(state["keyword"])
        return state

    def score(state):
        state["scored_signals"] = [score_signal(s) for s in state["raw_signals"]]
        state["selected_signal"] = max(
            state["scored_signals"], key=lambda s: s.composite
        )
        return state

    def validate(state):
        state["validated_facts"] = validate_signal(state["selected_signal"].url)
        return state

    def serp(state):
        angles, gaps = serp_gap_analysis(state["keyword"])
        state["competitor_angles"] = angles
        state["identified_gaps"] = gaps
        return state

    graph.add_node("discover", discover)
    graph.add_node("score", score)
    graph.add_node("validate", validate)
    graph.add_node("serp", serp)

    graph.set_entry_point("discover")
    graph.add_edge("discover", "score")
    graph.add_edge("score", "validate")
    graph.add_edge("validate", "serp")

    return graph.compile()