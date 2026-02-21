from fastapi import APIRouter
from app.graph import build_graph

router = APIRouter()

@router.post("/run-pipeline")
def run_pipeline(payload: dict):
    graph = build_graph()
    result = graph.invoke({"keyword": payload["keyword"]})
    return result