import time, requests

def measure_response_time(url: str) -> float:
    try:
        start = time.time()
        resp = requests.get(url, timeout=10)
        elapsed = time.time() - start
        return round(elapsed, 3)
    except Exception as e:
        return -1

def get_page_size(url: str) -> int:
    try:
        resp = requests.get(url, timeout=10)
        return len(resp.content)
    except Exception as e:
        return -1
