import os

from pydantic import BaseSettings


class GlobalConfig(BaseSettings):
    DB_HOST: str = os.getenv("DB_HOST")
    AWS_REGION: str = os.getenv("AWS_REGION", "ca-central-1")
    HASH_SALT: str = os.getenv("HASH_SALT", "My_Awesome_Salt_To_Change")
    DOMAIN: str = os.getenv("DOMAIN", "http://localhost:5000")


config = GlobalConfig()
