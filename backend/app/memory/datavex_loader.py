import json
from pathlib import Path

DATA_DIR = Path("data/datavex")

def load_datavex_memory():
    solutions = []

    # LinkedIn content
    linkedin_file = DATA_DIR / "segregated_posts.json"
    if linkedin_file.exists():
        with open(linkedin_file, "r", encoding="utf-8") as f:
            posts = json.load(f)
            for tag, texts in posts.items():
                for text in texts:
                    solutions.append({
                        "source": "linkedin",
                        "tag": tag,
                        "content": text
                    })

    # Website content
    website_file = DATA_DIR / "website_data.txt"
    if website_file.exists():
        with open(website_file, "r", encoding="utf-8") as f:
            solutions.append({
                "source": "website",
                "content": f.read()
            })

    return solutions