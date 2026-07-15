import logging, os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "cyberscope.log")

def setup_logger(level=logging.INFO):
    os.makedirs(LOG_DIR, exist_ok=True)
    logger = logging.getLogger("CyberScope")
    logger.setLevel(level)
    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(level)
    fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
