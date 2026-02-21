from typing import List
from app.models.signal import Signal, ScoredSignal
from app.models.strategy import StrategyBrief


class PipelineState(dict):
    keyword: str
    raw_signals: List[Signal]
    scored_signals: List[ScoredSignal]
    selected_signal: ScoredSignal
    validated_facts: List[str]
    competitor_angles: List[str]
    identified_gaps: List[str]
    strategy_brief: StrategyBrief