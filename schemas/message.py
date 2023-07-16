from typing import Optional, List, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

from schemas.document import Document
from schemas.block import RecognitionBlock, Block
from schemas.theme import RecognitionTheme
from schemas.location import RecognitionLocation, ApprovedLocation


# Shared properties
class MessageBase(BaseModel):
    text: str


class MessageCreate(MessageBase):
    
    document: Document


class MessageSchema(MessageBase):
    id: UUID
    created_at: datetime 
    recognition_blocks: List[Optional[RecognitionBlock]]
    recognition_themes: List[Optional[RecognitionTheme]]
    recognition_locations: List[Optional[RecognitionLocation]]
    approved_block: Optional[str]
    approved_theme: Optional[str]
    approved_location: Optional[ApprovedLocation]


    class Config:
        orm_mode = True

