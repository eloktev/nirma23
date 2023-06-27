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

@router.get("/{document_id}/events", response_model=Optional[EventsSchema])
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

@router.get("/{document_id}/file", 
            response_class=FileResponse
            )
def export_document_messages(document_id: UUID,
                          db: Session = Depends(deps.get_db)):
    """
    Retrieve a file with messages of a document with fileId
    """
    document = dao.dao_document.get(db, id=document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    elif document.status == DocumentStatus.loaded:
        raise HTTPException(status_code=425, detail="Markup in progress for this document")
    
    messages = dao.dao_message.get_by_file_id(db, document_id=document_id)
    data = {
        "Дата создания": [],
        "ID": [],
        "Текст": [],
        "Утвержденный блок": [],
        "Утвержденная тема": [],
        "Утвержденная локация": [],
        "Блок": [],
        "Тема": [],
        "Локация": []
    }
    for msg in messages:
        data["Дата создания"].append(msg.created_at)
        data["ID"].append(msg.id)
        data["Текст"].append(msg.text)
        data["Утвержденный блок"].append(msg.approved_block)
        data["Утвержденная тема"].append(msg.approved_theme)
        data["Утвержденная локация"].append(msg.approved_location)
        blocks = msg.recognition_blocks
        block_str = ""
        for block in blocks:
            block_probabilty = "%.2f" % round(block.probability, 2)
            block_str += f"{block.name} ({block_probabilty} %) "
        data["Блок"].append(block_str)
        themes = msg.recognition_themes
        theme_str = ""
        for theme in themes:
            theme_probabilty = "%.2f" % round(theme.probability, 2)
            theme_str += f"{theme.name} ({theme_probabilty} %) "
        data["Тема"].append(theme_str)
        locations = msg.recognition_locations
        location_str = ""
        for location in locations:
            location_probabilty = "%.2f" % round(location.probability, 2)
            location_str += f"{location.street_name} ({location_probabilty} %) "

        data["Локация"].append(location_str)

    df = pandas.DataFrame.from_dict(data)
    stream = io.BytesIO()

    writer = pandas.ExcelWriter('temp.xlsx', engine='xlsxwriter')
    writer.book.filename = stream

    df.to_excel(writer, index = False)
    writer.close()
    stream.seek(0)
    # response = StreamingResponse(iter([stream.getvalue()]),
                                #  media_type="text/csv"
                                # )
    # response.headers["Content-Disposition"] = f"attachment; filename={document_id}.csv"
    return Response(stream.getvalue(),  headers={'Content-Disposition': 'attachment; filename="%s.xlsx"' %(document_id)})

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
