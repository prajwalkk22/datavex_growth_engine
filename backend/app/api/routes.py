# from fastapi import APIRouter
# from backend.app.graph import build_graph
# from backend.app.agents.pain_solution_matcher import match_pain_to_solution

# router = APIRouter()

# # -------------------------------
# # 🚀 Production pipeline
# # -------------------------------
# @router.post("/run-pipeline")
# def run_pipeline(payload: dict):
#     graph = build_graph()
#     result = graph.invoke({"keyword": payload["keyword"]})
#     return result


# # -------------------------------
# # 🔍 DEBUG: Pain → Solution Match
# # (NO LLM, NO API COST)
# # -------------------------------
# @router.post("/debug/solution-match")
# def debug_solution_match(payload: dict):
#     gaps = payload.get("gaps", [])
#     matches = match_pain_to_solution(gaps)

#     return {
#         "gaps": gaps,
#         "matches": matches
#     }

from fastapi import APIRouter
from pydantic import BaseModel
import os

from backend.app.graph import build_graph
from backend.app.agents.pain_solution_matcher import match_pain_to_solution
from backend.app.approval import approval_and_publish

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


# -------------------------------
# 🧪 DEBUG: LinkedIn Post (Selenium)
# curl-triggerable, NO pipeline
# -------------------------------

class LinkedInDebugPost(BaseModel):
    text: str
    auto_approve: bool = False


@router.post("/debug/linkedin")
def debug_linkedin_post(payload: LinkedInDebugPost):
    """
    Debug-only endpoint to test LinkedIn Selenium posting.
    """

    # 🔒 Safety guard (strongly recommended)
    if os.getenv("ENV", "local") != "local":
        return {"error": "LinkedIn debug endpoint disabled"}

    if payload.auto_approve:
        # Bypass terminal input
        approval_and_publish(payload.text)
    else:
        # Will ask: Approve blog? (yes/no)
        approval_and_publish(payload.text)

    return {
        "status": "triggered",
        "message": "LinkedIn automation started"
    }