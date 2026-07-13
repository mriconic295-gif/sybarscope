from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os

SCREENSHOTS_DIR = "screenshots"

def take_screenshot(url: str, filename: str) -> str:
    """Returns path to screenshot file."""
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOTS_DIR, f"{filename}.png")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        driver.save_screenshot(filepath)
        driver.quit()
        return filepath
    except Exception as e:
        return f"Error: {str(e)}"
