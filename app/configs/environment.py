"""
Module to load all Environment variables
"""
from typing import Optional

from pydantic import BaseSettings, Field

from __version__ import version


class Environment(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    APPLICATION_HOST: str = Field(default="0.0.0.0")
    APPLICATION_PORT: int = Field(default=8000)
    APPLICATION_NAME = Field(default="fastapiexample", required=False)
    APPLICATION_VERSION = version
    LOG_LEVEL: Optional[str] = Field(default="error")
    LOG_DIR: str = Field(default="/var/log/smarket")

    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
