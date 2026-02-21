import os
import json
from google import genai
from backend.app.models.strategy import StrategyBrief

# Official Gemini client (FREE tier works)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
You are an expert growth strategist inside DataVex.

Rules:
- Do NOT choose obvious angles
- Explicitly reject weak or saturated angles
- Exploit SERP gaps competitors ignore
- Write in a confident, technical tone
- Return ONLY valid JSON
- platform_distribution_plan values MUST be strings
- target_audience MUST be a single string
"""


def normalize_strategy_json(data: dict) -> dict:
    # Fix platform_distribution_plan
    if isinstance(data.get("platform_distribution_plan"), dict):
        for k, v in data["platform_distribution_plan"].items():
            if isinstance(v, dict):
                data["platform_distribution_plan"][k] = " ".join(
                    f"{key}: {val}" for key, val in v.items()
                )

    # Fix target_audience
    if isinstance(data.get("target_audience"), list):
        data["target_audience"] = ", ".join(data["target_audience"])

    # ✅ FIX competitive_gap_exploited (list → string)
    if isinstance(data.get("competitive_gap_exploited"), list):
        data["competitive_gap_exploited"] = "; ".join(
            data["competitive_gap_exploited"]
        )

    return data


def generate_strategy_brief(
    keyword: str,
    selected_signal,
    identified_gaps: list[str],
):
    signal = selected_signal.dict()

    prompt = f"""
SYSTEM:
{SYSTEM_PROMPT}

Keyword: {keyword}

Selected Signal:
Title: {signal["title"]}
Summary: {signal["summary"]}

Identified SERP Gaps:
{identified_gaps}

Return JSON with fields:
- signal_summary
- chosen_angle
- angle_rationale
- rejected_angles (min 2, each with angle + reason)
- competitive_gap_exploited
- core_positioning_thesis
- platform_distribution_plan (blog, linkedin, twitter as STRINGS)
- target_audience (STRING)
- estimated_authority_score (0-100)
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    text = response.text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    data = json.loads(text)
    data = normalize_strategy_json(data)

    return StrategyBrief(**data)