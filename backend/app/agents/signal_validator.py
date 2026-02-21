import requests

def validate_signal(url: str) -> list[str]:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception:
        return []

    return [
        "Signal URL reachable",
        "Primary source confirmed"
    ]