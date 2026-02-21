from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def generate_blog(strategy_brief):
    prompt = f"""
You are a senior technical writer at DataVex.

Write an 800–1200 word blog using this strategy:

Chosen Angle:
{strategy_brief.chosen_angle}

Core Thesis:
{strategy_brief.core_positioning_thesis}

Rules:
- Problem-first hook (first 2 sentences)
- Technical depth for RevOps + Data teams
- No salesy language
- Clear H1/H2/H3 structure
- CTA at the end (non-salesy)
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    return response.text.strip()