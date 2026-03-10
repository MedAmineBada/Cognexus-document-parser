"""
This module defines the API routes for text extraction.
"""
from fastapi import APIRouter, UploadFile, File

from api.v1.services.textx_services import extract_text

router = APIRouter()

@router.post("/scan")
async def scan(file: UploadFile = File(...)):
    """
    Handles file uploads for text extraction.

    Args:
        file: The uploaded file.

    Returns:
        The extracted text.
    """
    return await extract_text(file)
