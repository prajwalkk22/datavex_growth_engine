from google import genai
import os
import json

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"

CRITIQUE_PROMPT = """
You are a demanding editorial director.

Score the blog on:
- Hook Strength
- Clarity
- Authority Tone
- Differentiation
- Logical Structure
- Brand Fit

Return ONLY JSON:
{
  "scores": { "Hook Strength": 0-10, ... },
  "rewrite_instructions": [ "...", "..." ]
}
"""


def critique_blog(blog_text):
    response = client.models.generate_content(
        model=MODEL,
        contents=f"{CRITIQUE_PROMPT}\n\nBLOG:\n{blog_text}",
    )

    text = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(text)