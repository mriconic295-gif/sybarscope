import requests

def detect_cdn(url: str) -> list:
    try:
        resp = requests.get(url, timeout=5)
        headers = resp.headers
        cdn_names = {
            "cloudflare": "Cloudflare",
            "akamai": "Akamai",
            "fastly": "Fastly",
            "stackpath": "StackPath",
            "keycdn": "KeyCDN",
            "cdn77": "CDN77"
        }
        detected = []
        server = headers.get("Server", "")
        via = headers.get("Via", "")
        for key, name in cdn_names.items():
            if key in server.lower() or key in via.lower():
                detected.append(name)
        # Check CF-Ray header
        if "CF-Ray" in headers:
            detected.append("Cloudflare")
        return detected
    except Exception as e:
        return [f"Error: {str(e)}"]
