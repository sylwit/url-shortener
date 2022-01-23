import os

from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    AWS_REGION: str = os.getenv("AWS_REGION", "ca-central-1")


config = GlobalConfig()
