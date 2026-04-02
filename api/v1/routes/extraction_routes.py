"""
This module defines the API routes for text extraction.
"""
from fastapi import APIRouter, UploadFile, File
from starlette import status

from api.v1.services.extraction_services import extract_content

router = APIRouter()

@router.post("/extract", status_code=status.HTTP_200_OK)
async def extract(file: UploadFile = File(...)):
    return await extract_content(file)
