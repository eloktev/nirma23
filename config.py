import secrets
from typing import Any, Dict, List, Optional, Union
import os
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class CommonSettings(BaseSettings):
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    PROJECT_NAME: str = "НИРМА 2023"

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    class Config:
        case_sensitive = True


class LocalSettings(CommonSettings):
    SQLALCHEMY_DATABASE_URI: Optional[str] = "sqlite:///./sql_app.db"

class StageSettings(CommonSettings):
    SQLALCHEMY_DATABASE_URI: Optional[str] = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:5432/{os.getenv('POSTGRES_DB')}"


settings = StageSettings()
