import requests
from bs4 import BeautifulSoup
from pathlib import Path

URL = "https://datavex.ai/"
OUTPUT_PATH = Path("backend/data/datavex/website_data.txt")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; DataVexBot/1.0)"
}

response = requests.get(URL, headers=headers, timeout=15)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# Remove junk
for tag in soup(["script", "style", "nav", "footer", "noscript"]):
    tag.decompose()

title = soup.title.string if soup.title else "No Title"

paragraphs = [
    p.get_text(strip=True)
    for p in soup.find_all("p")
    if len(p.get_text(strip=True)) > 40
]

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write(f"SOURCE: {URL}\n")
    f.write(f"TITLE: {title}\n\n")

    for para in paragraphs:
        f.write(para + "\n\n")

print(f"✅ Website scraped: {len(paragraphs)} paragraphs saved")