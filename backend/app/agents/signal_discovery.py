import requests
from backend.app.config import TAVILY_API_KEY
from backend.app.models.signal import Signal

def discover_signals(keyword: str) -> list[Signal]:
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": keyword,
            "search_depth": "advanced",
            "max_results": 5
        },
        timeout=30
    )

    data = response.json()

    signals = []
    for r in data.get("results", []):
        signals.append(
            Signal(
                title=r["title"],
                url=r["url"],
                date=r.get("published_date", "unknown"),
                summary=r["content"][:300],
                relevance_score=7.0
            )
        )

    return signals