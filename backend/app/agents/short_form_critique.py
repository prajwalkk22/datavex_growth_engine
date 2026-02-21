from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

CRITIQUE_PROMPT = """
Score this content on:
- Hook Density
- Platform Fit
- Engagement Triggers
- Shareability
- Brand Fit

Return JSON only:
{
  "scores": { "Hook Density": 0-10, ... },
  "rewrite_instructions": []
}
"""


def critique(text):
    res = client.models.generate_content(
        model=MODEL,
        contents=f"{CRITIQUE_PROMPT}\n\n{text}"
    )
    clean = res.text.replace("```json", "").replace("```", "")
    return json.loads(clean)