from typing import Optional, List, Union

from fastapi import APIRouter, Body, Depends, BackgroundTasks, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.exceptions import HTTPException
from schemas.location import Location
import dao, models, schemas
from api import deps

from models.document import DocumentStatus

router = APIRouter()

@router.get("/{document_id}", response_model=List[Optional[schemas.message.MessageSchema]])
def get_document_messages(document_id: UUID,
                          db: Session = Depends(deps.get_db)):
    """
    Retrieve messages of a document with fileId
    """
    document = dao.dao_document.get(db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    elif document.status == DocumentStatus.loaded:
        raise HTTPException(status_code=425, detail="Markup in progress for this document")
    return dao.dao_message.get_by_file_id(db, document_id=document_id)


@router.patch("/{message_id}/approve/block", response_model=schemas.message.MessageSchema)
def approve_block(message_id: UUID,
                  value: str,
                  db: Session = Depends(deps.get_db)):
    message = dao.dao_message.get(db, id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found. Check that MESSAGE id is passed, not Document")

    a_block_obj = schemas.block.ApprovedBlockCreate(message_id=message_id, name=value)
    doc = dao.dao_document.get(db, id=message.document_id)
    if not dao.dao_document.has_approved_messages(db, id=doc.id):
        dao.dao_document.set_approve_start(db, uuid=doc.id)
    a_block = dao.dao_approvedblock.create(db, obj_in=a_block_obj)
    if dao.dao_document.is_every_approved_messages(db, id=doc.id):
        dao.dao_document.set_marked_up(db, uuid=doc.id)
    return a_block
    
@router.patch("/{message_id}/approve/theme", response_model=schemas.message.MessageSchema)
def approve_theme(message_id: UUID,
                  value: str,
                  db: Session = Depends(deps.get_db)):
    message = dao.dao_message.get(db, id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found. Check that MESSAGE id is passed, not Document")
    a_theme_obj = schemas.theme.ApprovedThemeCreate(message_id=message_id, name=value)
    doc = dao.dao_document.get(db, id=message.document_id)
    dao.dao_document.set_approve_start(db, uuid=doc.id)
    a_theme = dao.dao_approvedtheme.create(db, obj_in=a_theme_obj)
    if dao.dao_document.is_every_approved_messages(db, id=doc.id):
        dao.dao_document.set_marked_up(db, uuid=doc.id)
    return a_theme


@router.patch("/{message_id}/approve/location", response_model=schemas.message.MessageSchema)
def approve_location(message_id: UUID,
                  location: Location,
                  db: Session = Depends(deps.get_db)):
    message = dao.dao_message.get(db, id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found. Check that MESSAGE id is passed, not Document")
    a_location_obj = schemas.location.ApprovedLocationCreate(message_id=message_id, name = location.name, geometry=location.geometry)
    doc = dao.dao_document.get(db, id=message.document_id)
    if not dao.dao_document.has_approved_messages(db, id=doc.id):
        dao.dao_document.set_approve_start(db, uuid=doc.id)
    a_location = dao.dao_approvedlocation.create(db, obj_in=a_location_obj)
    if dao.dao_document.is_every_approved_messages(db, id=doc.id):
        dao.dao_document.set_marked_up(db, uuid=doc.id)
    return a_location
