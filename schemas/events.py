from typing import Optional, Union
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from schemas.document import Document

class EventsBase(BaseModel):
    file_events: bytes
    file_messages: bytes


class EventsCreate(EventsBase):
    document: Document
   




class Events(EventsBase):
    id: Union[str, UUID]

    class Config:
        orm_mode = True

