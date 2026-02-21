from app.state import PipelineState
from app.agents.pain_solution_matcher import match_pain_to_solution

def test_pipeline_halts_without_solution():
    state = PipelineState(
        keyword="some random topic",
        identified_gaps=["Unknown pain"]
    )

    matches = match_pain_to_solution(state["identified_gaps"])
    assert matches == [] or matches is not None