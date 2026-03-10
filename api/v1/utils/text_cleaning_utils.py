"""
This module provides utilities for cleaning and processing text using an external API.
"""
import httpx

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
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            env.LLMORC_API,
            json=payload
        )

    return response.json()
