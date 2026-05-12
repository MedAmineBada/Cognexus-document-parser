"""
This module defines custom exception classes for the API.

These exceptions are used to represent various error conditions that can occur
during the processing of an API request. The module also provides exception
handlers to ensure that these custom exceptions are caught and transformed into
appropriate HTTP responses.
"""
from http.client import HTTPException

from starlette import status
from starlette.responses import JSONResponse
from fastapi import Request

class CustomException(HTTPException):
    """Base class for custom exceptions with message and HTTP status code."""

    def __init__(self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, message: str = "Something went wrong"):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class UnprocessableContent(CustomException):
    """Exception raised for unprocessable content (422)."""
    def __init__(self, message: str ="The request content is unprocessable."):
        super().__init__(status.HTTP_422_UNPROCESSABLE_CONTENT, message)

class BadGatewayException(CustomException):
    """Exception raised for a bad gateway error (502)."""
    def __init__(self, message: str ="Failed to connect to upstream service."):
        super().__init__(status.HTTP_502_BAD_GATEWAY, message)

class GatewayTimeoutException(CustomException):
    """Exception raised for a gateway timeout error (504)."""
    def __init__(self, message: str ="Upstream service timed out."):
        super().__init__(status.HTTP_504_GATEWAY_TIMEOUT, message)

class PdfProcessingError(CustomException):
    """Exception raised for errors during PDF processing."""
    def __init__(self, message: str = "Could not process the PDF file."):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)

class PdfImageExtractionError(CustomException):
    """Exception raised for errors during image extraction from PDF."""
    def __init__(self, message: str = "Could not extract image from PDF."):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, message)

async def generic_exception_handler(request: Request, exc):
    """Handles unexpected exceptions, returning a 500 error."""
    print(f"Unexpected {type(exc).__name__}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Something went wrong."},
    )

async def custom_exception_handler(request: Request, exc):
    """Handles custom exceptions, returning the appropriate status and message."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )
