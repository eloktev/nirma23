from typing import Optional, List, Union

from fastapi import APIRouter, Body, Depends, BackgroundTasks, UploadFile
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi.exceptions import HTTPException
from schemas.location import Location
import dao, models, schemas
from api import deps
from fastapi.responses import Response, FileResponse, StreamingResponse
from models.document import DocumentStatus
import pandas, io

from schemas.events import Events as EventsSchema
router = APIRouter()

@router.get("/{document_id}", response_model=Optional[EventsSchema])
def get_document_events(document_id: UUID,
                          db: Session = Depends(deps.get_db)):
    """
    Retrieve risk events
    """
    document = dao.dao_document.get(db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    elif document.status == DocumentStatus.loaded:
        raise HTTPException(status_code=425, detail="Markup in progress for this document")
    
    events = dao.dao_events.get_by_file_id(db, document_id=document_id)
    if not events:
        raise HTTPException(status_code=404, detail="Events for document not found")

    return events
