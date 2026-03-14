"""
This module defines the environment variables for the application.
"""
from pydantic.v1 import BaseSettings


class EnvFile(BaseSettings):
    """
    Defines the environment variables for the application.
    """
    EXGATE_LLM_URL: str
    EXGATE_CLOUDINARY_URL: str

    EXAM_FOLDER: str
    CORRECTION_FOLDER: str


    class Config:
        """
        Specifies the environment file to use.
        """
        env_file = ".env"

"""An instance of the EnvFile class, providing access to the environment variables."""
env = EnvFile()
