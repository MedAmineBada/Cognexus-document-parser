"""
This module provides services for extracting and processing text from PDF files.
"""
import base64
import json

import fitz
from fastapi import UploadFile

from api.v1.utils import clean_text, organize_text_prompt, extract_pages_from_document
from api.v1.utils.exceptions import UnprocessableContent, CustomException
from api.v1.utils.image_utils import upload_images
from config import env


async def extract_content(file: UploadFile) -> dict:
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
        doc = fitz.open(stream=content, filetype="pdf")

    except Exception as e:
        raise CustomException(message="Something went wrong: could not process the PDF.")

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


async def extract_images(file: UploadFile, exam_id: int):
    if not file.content_type == "application/pdf":
        raise UnprocessableContent(message="file must be of type PDF.")
    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as e:
        print(e)
        raise CustomException(message="Something went wrong: could not process the PDF.")

    images = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_info_list = page.get_image_info(xrefs=True)
        image_info_list.sort(key=lambda info: (info["bbox"][1], info["bbox"][0]))

        for info in image_info_list:
            xref = info["xref"]
            if xref == 0:
                continue
            try:
                base_image = doc.extract_image(xref)
                images.append(
                    base64.b64encode(base_image["image"]).decode("utf-8")
                )

            except Exception:
                raise

    doc.close()
    return await upload_images(images, folder=f"{env.EXAM_FOLDER}/{exam_id}")
