from typing import Optional, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from models.document import DocumentStatus

# Shared properties
class DocumentBase(BaseModel):
    name: str


class DocumentCreate(DocumentBase):
    file: bytes


class Document(DocumentBase):
    id: Union[str, UUID]
    created_at: datetime
    status: DocumentStatus

    class Config:
        orm_mode = True

