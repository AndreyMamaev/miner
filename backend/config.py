import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DB_USER: str = os.getenv('POSTGRES_USER')
    DB_PASS: str = os.getenv('POSTGRES_PASSWORD')
    DB_HOST: str = os.getenv('POSTGRES_HOST')
    DB_PORT: str = os.getenv('POSTGRES_PORT')
    DB_NAME: str = os.getenv('POSTGRES_DB')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'allow'

s = Settings()
