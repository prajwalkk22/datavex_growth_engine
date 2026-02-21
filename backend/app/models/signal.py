from pydantic import BaseModel
from typing import List

class Signal(BaseModel):
    title: str
    url: str
    date: str
    summary: str
    relevance_score: float

class ScoredSignal(Signal):
    authority: float
    recency: float
    relevance: float
    novelty: float
    composite: float