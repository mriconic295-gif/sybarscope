import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

SCREENSHOTS_DIR = "screenshots"

def take_screenshot(url: str, filename: str) -> str:
    """
    GitHub રેડી સ્ક્રિનશોટ મોડ્યુલ. 
    યુઝરે કોઈ વધારાનો કમાન્ડ ચલાવવો નહીં પડે.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOTS_DIR, f"{filename}.png")
    
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # ૧. Selenium Headless Chrome 
    try:
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # webdriver-manager પોતે જ ક્રોમ ડ્રાઈવર સેટઅપ કરી લેશે
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)
        
        driver.get(url)
        driver.save_screenshot(filepath)
        driver.quit()
        
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return filepath
    except Exception as e:
        print(f"[Screenshot Warning] Local Chrome driver failed: {e}. Trying HTTP Render fallback...")

    # ૨. Backup Fallback (જો યુઝરના સિસ્ટમમાં ક્રોમ ડ્રાઈવરમાં એરર હોય તો)
    try:
        render_url = f"https://mini.s-shot.ru/1280x800/PNG/1024/Z100/?{url}"
        res = requests.get(render_url, timeout=12)
        if res.status_code == 200 and len(res.content) > 1000:
            with open(filepath, "wb") as f:
                f.write(res.content)
            return filepath
    except Exception as e:
        print(f"[Screenshot Error] Backup failed: {e}")

    return f"Error: Could not take screenshot for {filename}"
