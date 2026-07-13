import requests

class GeoIP:
    def __init__(self, ip: str):
        self.ip = ip

    def get_location(self) -> dict:
        try:
            resp = requests.get(f"https://ipinfo.io/{self.ip}/json", timeout=5)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
