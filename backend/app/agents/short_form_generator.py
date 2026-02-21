from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-2.5-flash"


def generate_linkedin(strategy_brief):
    prompt = f"""
Write a LinkedIn post (200–300 words).

Rules:
- Strong hook in first line
- Short paragraphs
- One data-backed insight
- Practitioner tone (not salesy)
- End with discussion CTA

Strategy:
{strategy_brief.chosen_angle}
"""
    return client.models.generate_content(model=MODEL, contents=prompt).text


def generate_twitter(strategy_brief):
    prompt = f"""
Write a Twitter/X thread (6–8 tweets).

Rules:
- Tweet 1 = hook
- Numbered tweets
- <280 chars each
- Final tweet = CTA

Strategy:
{strategy_brief.chosen_angle}
"""
    text = client.models.generate_content(model=MODEL, contents=prompt).text
    return [t.strip() for t in text.split("\n") if t.strip()]