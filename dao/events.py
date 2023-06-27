from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from dao.base import BaseDAO
from models.events import Events
from schemas.events import EventsCreate, Events as EventsSchema
# from models.document import Document, DocumentStatus
# from models.message import Message
# from schemas.document import DocumentCreate

from datetime import datetime

class EventsDAO(BaseDAO[Events, EventsCreate, EventsCreate]):
    
    def get_by_file_id(self,  db: Session, *, document_id: str) -> Optional[Events]:
        return db.query(self.model).filter(self.model.document_id == document_id).first()

    def create(self, db: Session, *, obj_in: EventsCreate) -> Events:
        events = Events(
            document=obj_in.document,
            file_events=obj_in.file_events,
            file_messages=obj_in.file_messages,
            created_at=datetime.now(),
        )
        db.add(events)
        db.commit()
        db.refresh(events)
        return events


dao_events = EventsDAO(Events)
