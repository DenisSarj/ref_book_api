from src.app.common.loggers import setup_console_logger
from src.configs import settings

debug_logger = setup_console_logger(name="debug_logger", level=settings.log_level)
