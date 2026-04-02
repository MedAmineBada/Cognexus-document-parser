"""
This module provides services for extracting and processing content from PDF files.
"""
import fitz
from fastapi import UploadFile

from api.v1.utils import UnprocessableContent, CustomException


async def extract_content(file: UploadFile) -> dict:
    """
    Extracts raw text content from a PDF file.
    """
    if file.content_type != "application/pdf":
        raise UnprocessableContent(message="File must be of type PDF.")

    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception:
        raise CustomException(message="Something went wrong: could not process the PDF.")

    pages: list[str] = []

    for page in doc:
        pages.append(page.get_text())

    doc.close()

    return {
        "filename": file.filename,
        "total_pages": len(pages),
        "pages": pages,
    }