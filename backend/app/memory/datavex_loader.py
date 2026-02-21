import json
from pathlib import Path

# backend/app/memory/datavex_loader.py
# Go up to: backend/
BASE_DIR = Path(__file__).resolve().parents[2]

# backend/data/datavex
DATA_DIR = BASE_DIR / "data" / "datavex"

def load_datavex_memory():
    solutions = []

    print("📂 Using DATA_DIR:", DATA_DIR)

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
    else:
        print("❌ Missing:", linkedin_file)

    # Website content
    website_file = DATA_DIR / "website_data.txt"
    if website_file.exists():
        with open(website_file, "r", encoding="utf-8") as f:
            solutions.append({
                "source": "website",
                "content": f.read()
            })
    else:
        print("❌ Missing:", website_file)

    print(f"🧠 DataVex memory loaded: {len(solutions)} items")
    return solutions