import json
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

LINKEDIN_PAGE = "https://www.linkedin.com/company/datavexai-pvt-ltd/posts/"
OUTPUT_PATH = Path("backend/data/datavex/segregated_posts.json")
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Browser setup
# ---------------------------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

try:
    # ---------------------------
    # Manual login
    # ---------------------------
    print("🔐 LOGIN to LinkedIn manually")
    driver.get("https://www.linkedin.com/login")
    input("👉 After login is complete and feed is visible, press ENTER here...")

    # ---------------------------
    # Verify login
    # ---------------------------
    if "login" in driver.current_url:
        raise Exception("❌ Login not completed. Still on login page.")

    print("✅ Login confirmed")

    # ---------------------------
    # Open company posts page
    # ---------------------------
    driver.get(LINKEDIN_PAGE)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    # ---------------------------
    # Scroll to load posts
    # ---------------------------
    for _ in range(8):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # ---------------------------
    # Extract posts (CORRECT selector)
    # ---------------------------
    posts = driver.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2")
    print(f"🧾 Found {len(posts)} posts")

    data = {}

    for post in posts:
        text = post.text.strip()
        if len(text) < 80:
            continue

        tag = "general"
        t = text.lower()

        if "revops" in t:
            tag = "revops"
        elif "ai" in t:
            tag = "ai"
        elif "data" in t:
            tag = "data"

        data.setdefault(tag, []).append(text)

    # ---------------------------
    # Save
    # ---------------------------
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ LinkedIn posts saved: {sum(len(v) for v in data.values())}")

finally:
    driver.quit()