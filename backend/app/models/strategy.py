from pydantic import BaseModel
from typing import List, Dict


class RejectedAngle(BaseModel):
    angle: str
    reason: str


class StrategyBrief(BaseModel):
    signal_summary: str
    chosen_angle: str
    angle_rationale: str
    rejected_angles: List[RejectedAngle]
    competitive_gap_exploited: str
    core_positioning_thesis: str
    platform_distribution_plan: Dict[str, str]
    target_audience: str
    estimated_authority_score: int