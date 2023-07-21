from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from sqlalchemy.orm import Session

from db.database import SessionLocal



def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
