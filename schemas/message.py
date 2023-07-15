from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from schemas.document import Document
from schemas.block import RecognitionBlock, Block
from schemas.theme import RecognitionTheme
from schemas.location import RecognitionLocation


# Shared properties
class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    
    document: Document


class MessageSchema(MessageBase):
    id: UUID
    created_at: datetime 
    recognition_blocks: List[Optional[RecognitionBlock]]
    recognition_themes: Optional[List[Optional[RecognitionTheme]]]
    recognition_locations: Optional[Any]
    approved_block: Optional[str]
    approved_theme: Optional[str]
    approved_location: Optional[Any]


    class Config:
        orm_mode = True

