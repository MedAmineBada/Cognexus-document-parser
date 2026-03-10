"""
This module provides services for extracting and processing text from PDF files.
"""
import json

import fitz
from fastapi import UploadFile
from api.v1.utils import clean_text, organize_text_prompt

async def extract_text(file: UploadFile) -> dict:
    """
    Extracts text and images from a PDF file, structures the content,
    and sends it to an AI service for cleaning and organization.

    Args:
        file: The uploaded PDF file.

    Returns:
        A dictionary containing the cleaned and structured text.
    """
    content = await file.read()

    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to open PDF: {e}")

    pages: list[dict] = []
    image_counter = 0

    for page_num in range(len(doc)):
        page = doc[page_num]
        page_dict = page.get_text("dict")
        blocks = page_dict["blocks"]

        blocks.sort(key=lambda b: (round(b["bbox"][1] / 10), b["bbox"][0]))

        page_content: list[dict] = []

        for block in blocks:
            if block["type"] == 0:
                block_lines: list[str] = []
                for line in block["lines"]:
                    line_text = "".join(span["text"] for span in line["spans"])
                    if line_text.strip():
                        block_lines.append(line_text.strip())
                if block_lines:
                    page_content.append({
                        "type": "text",
                        "content": "\n".join(block_lines)
                    })

            elif block["type"] == 1:
                image_counter += 1
                page_content.append({
                    "type": "image_placeholder",
                    "content": f"[IMAGE_{image_counter}]",
                    "image_number": image_counter
                })

        pages.append({
            "page_number": page_num + 1,
            "content": page_content
        })

    doc.close()

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
