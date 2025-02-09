from src.api.v1 import api_router as api_v1_router
from src.api.docs import router as docs_router
from src.api.monitoring import router as monitoring_router

from fastapi import APIRouter

router = APIRouter(prefix="/api")

router.include_router(api_v1_router)
router.include_router(docs_router)
router.include_router(monitoring_router)