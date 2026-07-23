import os
from playwright.sync_api import sync_playwright

SCREENSHOTS_DIR = "screenshots"

def take_screenshot(url: str, filename: str) -> str:
    """
    Playwright નો ઉપયોગ કરીને સુપર-ફાસ્ટ અને 
    ૧૦૦% સચોટ વેબસાઇટનો સ્ક્રિનશોટ લેશે.
    """
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOTS_DIR, f"{filename}.png")
    
    # URL બરાબર છે કે નહીં તે ચેક કરશે
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Playwright Context મેનેજર રન કરશે
    try:
        with sync_playwright() as p:
            # હેડલેસ ક્રોમિયમ લોન્ચ કરશે
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                # સ્ટાન્ડર્ડ ડેસ્કટોપ સાઇઝ
                viewport={"width": 1280, "height": 800},
                # મનુષ્ય જેવો યુઝર-એજન્ટ
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # 15 સેકન્ડનો ટાઇમઆઉટ સેટ કરશે, જેથી લૂપમાં ના ફસાઈ જાય
            # domcontentloaded=મેઇન કન્ટેન્ટ લોડ થાય ત્યાં સુધી રાહ જોશે
            page.goto(url, timeout=15000, wait_until="domcontentloaded")
            
            # ફક્ત વિઝિબલ એરિયાનો સ્ક્રિનશોટ લેશે
            page.screenshot(path=filepath, full_page=False)
            
            browser.close()
            
            # જો ફાઇલ સેવ થઈ હોય અને સાઇઝ ૦ કરતાં વધારે હોય તો પાથ રિટર્ન કરશે
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                return filepath
                
    except Exception as e:
        print(f"[Screenshot Error] Playwright attempt failed: {e}. Trying fallback API...")
        # જો Playwright ફેલ જાય, તો એક ફ્રી API થી સ્ક્રીનશોટ પાડવાની કોશિશ કરશે, જેથી યુઝરને કોઈ એરર ના દેખાય.
        try:
            render_url = f"https://mini.s-shot.ru/1280x800/PNG/1024/Z100/?{url}"
            import requests
            res = requests.get(render_url, timeout=10)
            if res.status_code == 200 and len(res.content) > 1000:
                with open(filepath, "wb") as f:
                    f.write(res.content)
                return filepath
        except:
            pass

    return f"Error: Could not take screenshot for {filename}"
