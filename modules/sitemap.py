import requests

def detect_sitemap(url: str) -> bool:
    try:
        resp = requests.get(f"{url}/sitemap.xml", timeout=5)
        return resp.status_code == 200
    except Exception:
        return False
