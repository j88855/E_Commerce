import logging
from logging.handlers import RotatingFileHandler
import os

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger = logging.getLogger("ecommerce_logger")
            logger.setLevel(logging.DEBUG)
            # Formatter
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                "%Y-%m-%d %H:%M:%S"
            )

            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

            # File handler
            fh = RotatingFileHandler(
                os.path.join(LOG_DIR, "app.log"),
                maxBytes=5 * 1024 * 1024,  # 5 MB
                backupCount=5,
                encoding="utf-8"
            )
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            cls._instance = logger
        return cls._instance

# 全域 logger
logger = Logger()