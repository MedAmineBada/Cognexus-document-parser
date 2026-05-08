"""
Main application file for the Cognexus-TextX FastAPI service.
"""

from http.client import HTTPException

import uvicorn
from fastapi import FastAPI

from api.v1.utils.exceptions import custom_exception_handler, generic_exception_handler
from api.v1.v1_router import router

app = FastAPI(debug=False)


app.add_exception_handler(HTTPException, custom_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8012,
    )
