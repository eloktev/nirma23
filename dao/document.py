from typing import Any, Dict, Optional, Union, List

from sqlalchemy.orm import Session

from dao.base import BaseDAO
from models.document import Document, DocumentStatus
from models.message import Message
from schemas.document import DocumentCreate

from datetime import datetime

class DocumentDAO(BaseDAO[Document, DocumentCreate, DocumentCreate]):

    def get_by_id_and_status(self, db: Session, *, uuid: str, status: str) -> Optional[Document]:
        return db.query(Document).filter((Document.id == uuid) & (Document.status == status) ).first()
    
    def has_approved_messages(self, db: Session, *, id: str):
        return db.query(Document)\
                                .filter(Document.id == id)\
                                .filter(Document.messages.any(
                                            (Message.block_id != None) | 
                                            (Message.theme_id != None) |
                                            (Message.location_id != None))
                                ).first()
    def is_every_approved_messages(self, db: Session, *, id: str):
        return db.query(Document)\
                                .filter(Document.id == id)\
                                .filter(Document.messages.any(
                                            (Message.block_id != None) & 
                                            (Message.theme_id != None) )
                                ).first()




    
    def set_marking_up(self, db: Session, *, uuid: str) -> Document:
        doc = db.query(Document).filter((Document.id == uuid)).first()
        doc.status = DocumentStatus.markingup
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    def set_marked_up(self, db: Session, *, uuid: str) -> Document:
        doc = db.query(Document).filter((Document.id == uuid)).first()
        doc.status = DocumentStatus.approve
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    
    def set_approve_start(self, db: Session, *, uuid: str) -> Document:
        doc = db.query(Document).filter((Document.id == uuid)).first()
        doc.status = DocumentStatus.approving
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc

    
    def create(self, db: Session, *, obj_in: DocumentCreate) -> Document:
        document = Document(
            name=obj_in.name,
            file=obj_in.file,
            created_at=datetime.now(),
            status=DocumentStatus.loaded,
        )
        db.add(document)
        db.commit()
        db.refresh(document)
        return document


dao_document = DocumentDAO(Document)
