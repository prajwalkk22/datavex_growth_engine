from typing import List, Dict, Any
from app.models.signal import Signal, ScoredSignal

class PipelineState(dict):
    keyword: str
    raw_signals: List[Signal]
    scored_signals: List[ScoredSignal]
    selected_signal: ScoredSignal
    validated_facts: List[str]
    competitor_angles: List[str]
    identified_gaps: List[str]