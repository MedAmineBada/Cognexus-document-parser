"""
This module defines the environment variables for the application.
"""
from pydantic.v1 import BaseSettings


class EnvFile(BaseSettings):
    """
    Defines the environment variables for the application.
    """
    LLMORC_API: str
    """The URL of the LLMORC API."""

    class Config:
        """
        Specifies the environment file to use.
        """
        env_file = ".env"

env = EnvFile()
"""An instance of the EnvFile class, providing access to the environment variables."""