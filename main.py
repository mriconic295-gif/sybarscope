#!/usr/bin/env python3
"""
CyberScope - Cybersecurity Reconnaissance & Intelligence Tool
Main Entry Point
"""

import sys
import os

# 📍 Project Directory Path Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from utils.logger import setup_logger
from config.settings import load_config
from gui.app import App


def main():
    # 1. Logger આસાનીથી સેટઅપ કરો
    logger = setup_logger()
    logger.info("⚡ CyberScope Starting Up...")

    try:
        # 2. કન્ફિગરેશન સેટિંગ્સ લોડ કરો
        config = load_config()
        logger.info("✅ Configuration loaded successfully.")

        # 3. CustomTkinter App ઓપન કરો
        logger.info("🚀 Launching CyberScope Application GUI...")
        app = App(config)
        app.run()

    except Exception as e:
        logger.critical(f"❌ Unhandled Exception in Main Application: {str(e)}", exc_info=True)
        print(f"\n[CRITICAL ERROR] Failed to launch CyberScope: {e}")
        sys.exit(1)

    finally:
        logger.info("🛑 CyberScope Closed cleanly.")


if __name__ == "__main__":
    main()
