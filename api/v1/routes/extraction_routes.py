"""
This module defines the API routes for text extraction.
"""

from fastapi import APIRouter, UploadFile, File, Query
from starlette import status

from api.v1.services.extraction_services import extract_text, extract_all

router = APIRouter()


@router.post("/extract", status_code=status.HTTP_200_OK)
async def extract(
    file: UploadFile = File(...),
    mode: str = Query(default="text", enum=["text", "all"]),
):
    if mode == "all":
        return await extract_all(file)
    return await extract_text(file)
