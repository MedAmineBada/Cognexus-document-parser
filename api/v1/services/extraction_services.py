"""
This module provides services for extracting and processing text from PDF files.
"""
import json

import fitz
from fastapi import UploadFile
from api.v1.utils import clean_text, organize_text_prompt, extract_pages_from_document
from api.v1.utils.exceptions import UnprocessableContent, CustomException


async def extract_text(file: UploadFile) -> dict:
    """
    Extracts text and images from a PDF file, structures the content,
    and sends it to an AI service for cleaning and organization.

    Args:
        file: The uploaded PDF file.

    Returns:
        A dictionary containing the cleaned and structured text.
    """
    if not file.content_type == "application/pdf":
        raise UnprocessableContent(message="File must be of type PDF.")

    try:
        content = await file.read()
    except Exception as e:
        raise CustomException(message="Something went wrong: could not read the uploaded file.")

    try:
        doc = fitz.open(stream=content, filetype="pdf")

    except Exception as e:
        raise CustomException(message="Something went wrong: could not open the PDF.")

    pages = extract_pages_from_document(doc)

    image_counter = sum(1 for page in pages for item in page["content"] if item["type"] == "image_placeholder")

    res = {
        "filename": file.filename,
        "total_pages": len(pages),
        "total_images": image_counter,
        "pages": pages
    }

    base_prompt = organize_text_prompt

    exam_json = json.dumps(res, indent=2)

    prompt = base_prompt + exam_json

    cleaned_result = await clean_text(prompt)

    return cleaned_result

async def extract_images(file: UploadFile):
    pass