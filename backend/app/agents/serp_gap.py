import requests
from backend.app.config import TAVILY_API_KEY

def serp_gap_analysis(keyword: str):
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": keyword,
            "search_depth": "basic",
            "max_results": 10
        },
        timeout=30
    )

    data = response.json()
    angles = [r["title"] for r in data.get("results", [])]

    gaps = [
        "Operational impact not discussed",
        "No real-time signal analysis",
        "Missing RevOps execution layer"
    ]

    return angles, gaps