import logging

from os import PathLike
from pathlib import Path

from src.configs import settings, LOG_DEFAULT_FORMAT

logs_dir = Path(settings.logs_dir)


def setup_file_logger(name: str, log_file: PathLike, level: int = settings.log_level):
    log_file_path = logs_dir / log_file
    handler = logging.FileHandler(filename=log_file_path, encoding="utf-8", mode="a")
    handler.setFormatter(LOG_DEFAULT_FORMAT)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
