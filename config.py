import secrets
from typing import Any, Dict, List, Optional, Union

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
    SQLALCHEMY_DATABASE_URI: Optional[str] = "postgresql://postgres:postgres@10.200.0.235:5432/nirma_23"


settings = StageSettings()
