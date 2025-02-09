from fastapi import APIRouter
from src.api.v1.ref_book_router import router as ref_book_router

router = APIRouter(prefix="/v1")

router.include_router(ref_book_router)
