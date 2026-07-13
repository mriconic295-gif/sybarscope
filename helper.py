import re, tldextract

def extract_domain(url: str) -> str:
    """Extract domain from URL."""
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def is_valid_url(url: str) -> bool:
    pattern = r"^(https?://)?([\w\-]+\.)+[\w\-]+(/[\w\-\.~:/?#\[\]@!$&'()*+,;=]*)?$"
    return re.match(pattern, url) is not None
