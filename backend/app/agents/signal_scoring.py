from backend.app.models.signal import Signal, ScoredSignal
from datetime import datetime

def score_signal(signal: Signal) -> ScoredSignal:
    authority = 8.0 if any(x in signal.url for x in ["techcrunch", "arxiv", "github"]) else 6.0
    relevance = signal.relevance_score
    novelty = 7.5
    recency = 8.0 if "2025" in signal.date or "2026" in signal.date else 6.0

    composite = round(
        0.3 * authority +
        0.25 * recency +
        0.25 * relevance +
        0.2 * novelty,
        2
    )

    return ScoredSignal(
        **signal.dict(),
        authority=authority,
        recency=recency,
        relevance=relevance,
        novelty=novelty,
        composite=composite
    )