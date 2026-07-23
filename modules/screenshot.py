import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 💡 Webdriver Manager ના લોક ફાઇલ પ્રોબ્લેમ અને લોગ્સને બંધ કરવા માટેના સેટિંગ્સ
os.environ['WDM_LOG'] = '0'
os.environ['WDM_LOCAL'] = '1'
os.environ['WDM_SSL_VERIFY'] = '0'

def take_screenshot(url: str, domain: str) -> str:
    """
    આપેલ URL નો સ્ક્રીનશોટ લેશે અને તેને screenshots/ ફોલ્ડરમાં સેવ કરશે.
    પહેલા Local Chrome Driver થી પ્રયાસ કરશે, જો નિષ્ફળ જાય તો Web API Fallback વાપરશે.
    """
    # 📁 સ્ક્રીનશોટ સેવ કરવા માટેનું ફોલ્ડર બનાવવું
    output_dir = "screenshots"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{domain.replace('.', '_')}.png"
    filepath = os.path.join(output_dir, filename)

    # 1️⃣ પ્રથમ પ્રયાસ: Local Selenium Chrome Driver
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")  # બેકગ્રાઉન્ડ મોડ
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,800")
        options.add_argument("--log-level=3")  # Console warnings બંધ કરવા

        # Driver Service ઇન્સ્ટોલ અને સ્ટાર્ટ કરવું
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(15)

        driver.get(url)
        driver.save_screenshot(filepath)
        driver.quit()
        return filepath

    except Exception as e:
        print(f"[Screenshot Warning] Local Chrome driver failed: {e}. Trying HTTP Render fallback...")

    # 2️⃣ બીજો પ્રયાસ (Fallback): Free API દ્વારા સ્ક્રીનશોટ લેવો
    try:
        api_url = f"https://api.microlink.io/?url={url}&screenshot=true"
        response = requests.get(api_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            image_url = data.get("data", {}).get("screenshot", {}).get("url")
            if image_url:
                img_data = requests.get(image_url, timeout=15).content
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                return filepath
    except Exception as fallback_err:
        print(f"[Screenshot Error] Fallback also failed: {fallback_err}")

    return "Screenshot Failed"
