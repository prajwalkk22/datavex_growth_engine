from typing import List
from backend.app.models.signal import Signal, ScoredSignal
from backend.app.models.strategy import StrategyBrief
from backend.app.models.blog import BlogDraft, BlogEvolution

class PipelineState(dict):
    keyword: str
    raw_signals: List[Signal]
    scored_signals: List[ScoredSignal]
    selected_signal: ScoredSignal
    validated_facts: List[str]
    competitor_angles: List[str]
    identified_gaps: List[str]
    strategy_brief: StrategyBrief
    blog_final: str
    blog_evolution: list[BlogEvolution]