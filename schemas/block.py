from typing import Optional, Union
from uuid import UUID
from pydantic import BaseModel


class Block(BaseModel):
    name: str

    class Config:
        orm_mode = True


class RecognitionBlockBase(BaseModel):
    probability: float


class RecognitionBlockCreate(RecognitionBlockBase):
    message_id: UUID
    name: str
    

class RecognitionBlock(RecognitionBlockBase):
    name: str

    class Config:
        orm_mode = True


class ApprovedBlockCreate(BaseModel):
    message_id: UUID
    name: str #Block.name


class ApprovedBlock(BaseModel):
    name: str #Block.name

