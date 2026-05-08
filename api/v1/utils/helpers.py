import fitz
from fastapi import UploadFile

from api.v1.utils import CustomException, UnprocessableContent


def _open_pdf(content: bytes) -> fitz.Document:
    """
    Attempts to open a PDF from bytes, raising a CustomException on failure.
    """
    try:
        return fitz.open(stream=content, filetype="pdf")
    except Exception:
        raise CustomException(
            message="Something went wrong: could not process the PDF."
        )


async def _read_pdf(file: UploadFile) -> tuple[str, bytes]:
    """
    Validates the file type and reads its bytes.
    Returns the filename and raw content.
    """
    if file.content_type != "application/pdf":
        raise UnprocessableContent(message="File must be of type PDF.")
    content = await file.read()
    return file.filename, content
