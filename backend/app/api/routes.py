from fastapi import APIRouter
from backend.app.graph import build_graph
from backend.app.agents.pain_solution_matcher import match_pain_to_solution

router = APIRouter()

# -------------------------------
# 🚀 Production pipeline
# -------------------------------
@router.post("/run-pipeline")
def run_pipeline(payload: dict):
    graph = build_graph()
    result = graph.invoke({"keyword": payload["keyword"]})
    return result


# -------------------------------
# 🔍 DEBUG: Pain → Solution Match
# (NO LLM, NO API COST)
# -------------------------------
@router.post("/debug/solution-match")
def debug_solution_match(payload: dict):
    gaps = payload.get("gaps", [])
    matches = match_pain_to_solution(gaps)

    return {
        "gaps": gaps,
        "matches": matches
    }