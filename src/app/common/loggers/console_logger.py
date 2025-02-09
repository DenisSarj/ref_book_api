import logging

from src.configs import settings, LOG_DEFAULT_FORMAT


def setup_console_logger(name: str, level: int = settings.log_level):
    logger = logging.getLogger(name)

    handler = logging.StreamHandler()
    handler.setFormatter(LOG_DEFAULT_FORMAT)

    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
