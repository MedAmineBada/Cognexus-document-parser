"""
This module defines the API routes for text extraction.
"""
from fastapi import APIRouter, UploadFile, File
from fastapi.params import Form, Query
from starlette import status

from api.v1.services.extraction_services import extract_content, extract_images

router = APIRouter()


@router.post("/extract", status_code=status.HTTP_200_OK)
async def extract(file: UploadFile = File(...)):
    return await extract_content(file)


@router.post("/images", status_code=status.HTTP_200_OK)
async def scan_image(file: UploadFile = File(...), exam_id: int = Form(...)):
    """
    Handles file uploads for image extraction.

    Args:
        file: The uploaded file.

    Returns:
        The extracted images.
        :param file:
        :param exam_id:
    """
    return await extract_images(file,exam_id)
