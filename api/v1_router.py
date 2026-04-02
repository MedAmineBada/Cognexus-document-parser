"""
API router for version 1 of the TextX service.
"""
from fastapi import APIRouter
from api.v1.routes import textx_router

router = APIRouter(prefix="/api/v1/doc")
router.include_router(textx_router)