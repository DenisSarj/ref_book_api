import uvicorn

from src.app.common.loggers import debug_logger
from src.configs import settings

logger = debug_logger


def start_app():
    uvicorn.run("src.app.core.application:ref_book_app.fastapi_app",
                host=settings.app_host,
                port=settings.app_port,
                reload=settings.debug)


if __name__ == "__main__":
    logger.info("[#] Starting service...")
    logger.info(f"[#] DEBUG={settings.debug}")
    try:
        start_app()
    except KeyboardInterrupt:
        logger.info("[#] Stopped by user using keyboard.")
    except RuntimeError as e:
        logger.info(f"[X] {e}")
