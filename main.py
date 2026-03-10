"""
Main application file for the Cognexus-TextX FastAPI service.
"""
import logging
from http.client import HTTPException

from fastapi import FastAPI

from api.main_router import router
from api.v1.utils.exceptions import custom_exception_handler, generic_exception_handler


app = FastAPI(debug=False)


app.add_exception_handler(HTTPException, custom_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(router)

