from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    APPLICATION_HOST: str = Field(default="0.0.0.0")
    APPLICATION_PORT: int = Field(default=8000)
    APPLICATION_NAME: str = Field(default="GoldenRaspberryAwards", required=False)
