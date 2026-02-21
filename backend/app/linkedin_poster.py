from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# ⚠️ USE TEST ACCOUNT ONLY
EMAIL = "sharanabasavajkr99@gmail.com"
PASSWORD = "sharana_@123"

def post_to_linkedin(post_text: str):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    wait = WebDriverWait(driver, 20)

    try:
        # Login
        driver.get("https://www.linkedin.com/login")

        wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(EMAIL)
        driver.find_element(By.ID, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Open post composer
        driver.get("https://www.linkedin.com/feed/?shareActive=true")

        textbox = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )

        # ✅ FIX: Inject text via JavaScript (handles emojis & Unicode)
        driver.execute_script(
            """
            arguments[0].innerText = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            """,
            textbox,
            post_text
        )

        # Click Post
        post_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//span[text()='Post']]")
            )
        )
        post_button.click()

        time.sleep(5)

    finally:
        driver.quit()