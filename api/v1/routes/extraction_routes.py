"""
This module defines the API routes for text extraction.
"""
from fastapi import APIRouter, UploadFile, File
from fastapi.params import Form
from starlette import status

from api.v1.services.extraction_services import extract_text, extract_images
from api.v1.utils.exceptions import CustomException, NotFoundException

router = APIRouter()


@router.post("/text", status_code=status.HTTP_200_OK)
async def scan_text(file: UploadFile = File(...)):
    """
    Handles file uploads for text extraction.

    Args:
        file: The uploaded file.

    Returns:
        The extracted text.
    """
    return await extract_text(file)


@router.post("/images", status_code=status.HTTP_200_OK)
async def scan_image(file: UploadFile = File(...), exam_id: int = Form(...)):
    """
    Handles file uploads for image extraction.

    Args:
        file: The uploaded file.

    Returns:
        The extracted images.
    """
    return await extract_images(file,exam_id)
