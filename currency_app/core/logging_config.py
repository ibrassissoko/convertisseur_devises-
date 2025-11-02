"""
Module: logging_config.py
Responsabilité:
    Configuration globale du logging
"""

import logging

def setup_logging(level=logging.INFO):
    """Configure le logger global"""
    fmt = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    logging.basicConfig(level=level, format=fmt)
