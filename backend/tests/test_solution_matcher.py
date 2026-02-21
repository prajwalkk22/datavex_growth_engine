from app.agents.pain_solution_matcher import match_pain_to_solution

def test_solution_match_found():
    gaps = ["Missing RevOps execution layer"]

    matches = match_pain_to_solution(gaps)

    assert isinstance(matches, list)
    assert len(matches) > 0
    assert "solution" in matches[0]