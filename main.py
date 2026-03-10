"""
Main application file for the Cognexus-TextX FastAPI service.
"""
from fastapi import FastAPI

from api.main_router import router

app = FastAPI()

app.include_router(router)
