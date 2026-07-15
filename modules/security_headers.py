from config.constants import REQUIRED_SECURITY_HEADERS

def check_security_headers(headers: dict) -> dict:
    present = []
    missing = []
    for h in REQUIRED_SECURITY_HEADERS:
        if h in headers or h.lower() in headers:
            present.append(h)
        else:
            missing.append(h)
    return {"present": present, "missing": missing}
