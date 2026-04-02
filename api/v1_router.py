"""
API router for version 1 of the TextX service.
"""
from fastapi import APIRouter
from api.v1.routes import extraction_router

router = APIRouter(prefix="/api/v1/doc")
router.include_router(extraction_router)