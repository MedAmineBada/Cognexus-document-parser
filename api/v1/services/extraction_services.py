"""
This module provides services for extracting and processing content from PDF files.
"""

import base64

import fitz
from fastapi import UploadFile

from api.v1.utils import UnprocessableContent, CustomException
from api.v1.utils.helpers import _read_pdf, _open_pdf


async def extract_text(file: UploadFile) -> dict:
    """
    Extracts raw text content from a PDF file.
    """
    filename, content = await _read_pdf(file)
    doc = _open_pdf(content)

    pages: list[str] = []

    for page in doc:
        pages.append(page.get_text())

    doc.close()

    return {
        "filename": filename,
        "total_pages": len(pages),
        "pages": pages,
    }


async def extract_all(file: UploadFile) -> dict:
    if not file.content_type == "application/pdf":
        raise UnprocessableContent(message="file must be of type PDF.")
    try:
        content = await file.read()
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as e:
        print(e)
        raise CustomException(
            message="Something went wrong: could not process the PDF."
        )

    images = []
    full_text_parts = []
    image_index = 0

    for page_num in range(len(doc)):
        page = doc[page_num]

        image_info_list = page.get_image_info(xrefs=True)
        image_info_list.sort(key=lambda info: (info["bbox"][1], info["bbox"][0]))

        # Extract images and store their vertical position (y0) for ordering
        image_positions = []
        for info in image_info_list:
            xref = info["xref"]
            if xref == 0:
                continue
            try:
                base_image = doc.extract_image(xref)
                images.append(base64.b64encode(base_image["image"]).decode("utf-8"))

                image_positions.append(
                    {"y0": info["bbox"][1], "placeholder": f"$IMAGE_{image_index}$"}
                )
                image_index += 1
            except Exception:
                raise

        # Extract text blocks with their vertical position
        text_blocks = []
        raw_dict = page.get_text("dict", sort=True)
        for block in raw_dict["blocks"]:
            if block["type"] == 0:
                block_text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        block_text += span["text"]
                    block_text += "\n"
                block_text = block_text.strip()
                if block_text:
                    text_blocks.append({"y0": block["bbox"][1], "text": block_text})

        # Merge text blocks and image placeholders sorted by vertical position
        combined = []
        for tb in text_blocks:
            combined.append({"y0": tb["y0"], "content": tb["text"]})
        for ip in image_positions:
            combined.append({"y0": ip["y0"], "content": ip["placeholder"]})

        combined.sort(key=lambda x: x["y0"])
        full_text_parts.extend(item["content"] for item in combined)

    doc.close()

    return {
        "filename": file.filename,
        "total_images": len(images),
        "text": "\n".join(full_text_parts),
        "images": images,
    }
