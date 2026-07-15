import requests

def get_robots(url: str) -> str:
    try:
        resp = requests.get(f"{url}/robots.txt", timeout=5)
        return resp.text[:2000] if resp.status_code == 200 else "Not found"
    except Exception as e:
        return f"Error: {str(e)}"
