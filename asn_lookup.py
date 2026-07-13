import requests

def lookup_asn(ip: str) -> dict:
    try:
        resp = requests.get(f"https://ipapi.co/{ip}/json/", timeout=5)
        data = resp.json()
        return {
            "asn": data.get("asn"),
            "org": data.get("org"),
            "country": data.get("country")
        }
    except Exception as e:
        return {"error": str(e)}
