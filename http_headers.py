import requests

def get_headers(url: str) -> dict:
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return dict(resp.headers)
    except Exception as e:
        return {"error": str(e)}
