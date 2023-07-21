from typing import Optional, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from models.document import DocumentStatus

# from schemas.markup import Markup

class Theme(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RecognitionThemeBase(BaseModel):
    probability: float


class RecognitionThemeCreate(RecognitionThemeBase):
    message_id: UUID
    name: str


class RecognitionTheme(RecognitionThemeBase):
    name: str

    class Config:
        orm_mode = True


class ApprovedThemeCreate(BaseModel):
    message_id: UUID
    name: str #Theme.name


class ApprovedTheme(BaseModel):
    name: str #Theme.name


