import requests

class IPLookup:
    def __init__(self, ip: str):
        self.ip = ip

    def get_info(self) -> dict:
        # Free IP-API
        try:
            resp = requests.get(f"http://ip-api.com/json/{self.ip}", timeout=5)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
