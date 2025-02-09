from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.api import api_router
from src.app.common.loggers import setup_file_logger
from src.configs import settings


class RefBookApplication:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, debug: bool):
        self.debug = debug
        self.logger = setup_file_logger(
            name="ref_book_app_logger",
            log_file="application.log"
        )
        self._build_fastapi()

    @staticmethod
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.startup_func()
        yield
        await app.state.shutdown_func()

    def _build_fastapi(self):
        self.fastapi_app = FastAPI(
            title="API for Ref Book service",
            version=settings.app_version,
            docs_url=settings.app_docs_url,
            redoc_url=None
        )

        self.fastapi_app.include_router(api_router)
        self.fastapi_app.add_event_handler("startup", self._setup)
        self.fastapi_app.add_event_handler("shutdown", self._shutdown)

    def _setup(self):
        ...

    def _shutdown(self):
        ...
