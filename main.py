#!/usr/bin/env python3
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app import App
from utils.logger import setup_logger
from config.settings import load_config

def main():
    logger = setup_logger()
    logger.info("CyberScope starting...")
    config = load_config()
    app = App(config)
    app.run()

if __name__ == "__main__":
    main()
