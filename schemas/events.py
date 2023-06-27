from typing import Optional, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from schemas.document import Document



class EventsCreate(BaseModel):
    document: Document
    file_events: bytes
    file_messages: bytes


class Events(EventsCreate):
    id: Union[str, UUID]

    class Config:
        orm_mode = True

