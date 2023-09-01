from typing import Any, List

from fastapi import APIRouter, Body, Depends, BackgroundTasks, UploadFile
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session
from fastapi.responses import Response, FileResponse
from services.markupper import parse_document
import os
import logging
logger = logging.getLogger("gunicorn.error")
import dao, models, schemas
from api import deps
# from app.core.config import settings
# from app.utils import send_new_account_email

router = APIRouter()

MAP = {
    "а":"a",
    "б":"b",
    "в":"v",
    "г":"g",
    "д":"d",
    "е":"e",
    "ё":"yo",
    "ж":"zh",
    "з":"z",
    "и":"i",
    "й":"ij",
    "к":"k",
    "л":"l",
    "м":"m",
    "н":"n",
    "о":"o",
    "п":"p",
    "р":"r",
    "с":"s",
    "т":"t",
    "у":"u",
    "ф":"f",
    "х":"h",
    "ц":"tz",
    "ч":"ch",
    "ш":"sh",
    "щ":"tch",
    "ь":"",
    "ы":"y",
    "ъ":"",
    "э":"e",
    "ю":"yu",
    "я":"ya", 
}

@router.post("", response_model=schemas.Document)
async def create_document(file: UploadFile, 
                          background_tasks: BackgroundTasks,
                          db: Session = Depends(deps.get_db)):
    """
    Upload document.
    """
    doc = schemas.DocumentCreate(file=await file.read(), name=file.filename)
    doc_obj = dao.dao_document.create(db=db, obj_in=doc)
    background_tasks.add_task(parse_document, db, doc_obj)
    return doc_obj

@router.get("", response_model=list[schemas.Document])
def get_documents(db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> list[schemas.Document]:
    """
    Retrieve documents.
    """
    # documents = crud.document.get_multi(db, skip=skip, limit=limit)
    return dao.dao_document.get_multi(db, skip=skip, limit=limit)

@router.get("/{document_id}", response_model=schemas.Document)
def get_document(document_id: str, db: Session = Depends(deps.get_db),
):
    """
    Retrieve document by id.
    """
    doc_obj = dao.dao_document.get(db, id=document_id)
    return doc_obj

@router.get("/{document_id}/file", response_class=FileResponse)
def get_document_file(document_id: str, db: Session = Depends(deps.get_db),
):
    """
    Retrieve document file by id.
    """
    doc = dao.dao_document.get(db, id=document_id)
    file_name, file_extension = os.path.splitext(doc.name)
    file_name_safe = ""
    for c in file_name.upper():
        if c in MAP:
            file_name_safe += MAP[c]
        else:
            file_name_safe += c
    return Response(doc.file,  headers={'Content-Disposition': f'attachment; filename="{file_name_safe}{file_extension}"'})


@router.delete("/{document_id}", status_code=201)
def delete_document(document_id: str, db: Session = Depends(deps.get_db),
):
    """
    Delete document by id.
    """
    doc = dao.dao_document.remove(db, id=document_id)
    return None



