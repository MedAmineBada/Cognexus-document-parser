"""
This module provides utilities for cleaning and processing text using an external API.
"""
import httpx
import fitz
from httpx import ConnectError, TimeoutException

from api.v1.utils.exceptions import CustomException, BadGatewayException, GatewayTimeoutException
from config import env

async def clean_text(prompt: str):
    """
    Cleans the given text by sending it to the LLMORC API.

    Args:
        prompt: The text to be cleaned.

    Returns:
        The cleaned text as a JSON object.
    """
    payload = {
        "prompt": prompt
    }
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                env.EXGATE_LLM_URL,
                json=payload
            )

    except ConnectError:
        raise BadGatewayException(message="Failed to connect to LLMOrc service.")
    except TimeoutException:
        raise GatewayTimeoutException(message="LLMOrc service timed out.")

    if response.status_code != 200:
        try:
            body = response.json()
            message = body.get("error") or "Something went wrong within the LLMOrc Service."
        except Exception:
            message = "Something went wrong within the LLMOrc Service."

        raise CustomException(status_code=response.status_code,message=message)

    return response.json()

def extract_pages_from_document(doc: fitz.Document):
    """
    Extracts pages and their content from a given document.

    Args:
        doc: The document to extract pages from.

    Returns:
        A list of pages, where each page is a dictionary containing the page number and its content.
    """
    try:
        pages = []
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
                        "content": f"$IMGPHOLDER$[IMAGE_{image_counter}]",
                        "image_number": image_counter
                    })

            pages.append({
                "page_number": page_num + 1,
                "content": page_content
            })

        doc.close()

        return pages
    except Exception as e:
        raise CustomException(message="Something went wrong: could not extract pages from the document.")

from pathlib import PurePosixPath
