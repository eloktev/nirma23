from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session
from uuid import UUID
from dao.base import BaseDAO
from models.message import Message
from schemas.message import MessageCreate
from sqlalchemy import and_, or_, not_
from datetime import datetime
import logging

class MessageDAO(BaseDAO[Message, MessageCreate, MessageCreate]):
    
    def set_approved_block(self,  db: Session, *, message_id: UUID, approved_block_id: UUID) -> Optional[Message]:
        msg = db.query(self.model).filter(self.model.id == message_id).first()
        if msg:
            msg.block_id = approved_block_id
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return msg
        return None
    
    def set_approved_location(self,  db: Session, *, message_id: UUID, approved_location_id: UUID) -> Optional[Message]:
        msg = db.query(self.model).filter(self.model.id == message_id).first()
        if msg:
            msg.location_id = approved_location_id
            db.add(msg)
            db.commit()
            db.refresh(msg)
            return msg
        return None

    def set_approved_theme(self,  db: Session, *, message_id: UUID, approved_theme_id: UUID) -> Optional[Message]:
        msg = db.query(self.model).filter(self.model.id == message_id).first()
        if msg:
            msg.theme_id = approved_theme_id
            db.add(msg)
            db.commit()
            db.refresh(msg)
        return msg
    
    def get_by_file_id(self,  db: Session, *, document_id: str, block: Optional[str] = None) -> List[Optional[Message]]:
        if block:
            from dao.block import _dao_block
            logging.error(block)
            block = _dao_block.get_by_name(db, name=block)
            if not block:
                return []
            from models.block import RecognitionBlock

            logging.error(block.id)
            logging.error(block.name)
            messages = db.query(self.model).filter(self.model.document_id == document_id).all()
            return \
            db.query(self.model).filter(self.model.document_id == document_id).\
                join(RecognitionBlock).\
                filter(RecognitionBlock.id.in_([block]))
        else:
            return db.query(self.model).filter(self.model.document_id == document_id).all()

    def create(self, db: Session, *, obj_in: MessageCreate) -> Message:
        message = Message(
            created_at=datetime.now(),
            text=obj_in.text,
            document_id = obj_in.document.id
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message


dao_message = MessageDAO(Message)
