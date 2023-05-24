from fastapi import Depends, FastAPI, HTTPException, Form, File, UploadFile
import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import dao, models, schemas
from config import settings

from db.database import SessionLocal, engine
from db.base_class import Base
from typing import Annotated
from api.api_v1.api import api_router

# Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
    "https://nirma.lok-labs.com",
]


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

from api import deps

@app.get('/drop_data')
def drop_all_data(db: Session = Depends(deps.get_db)):
    """
    Dev function to remove all data
    """
    from models.document import Document
    from models.message import Message
    from models.block import Block, RecognitionBlock, ApprovedBlock
    from models.theme import Theme, RecognitionTheme, ApprovedTheme
    from models.location import Location, RecognitionLocation, ApprovedLocation
    db.query(RecognitionTheme).delete()
    db.query(RecognitionBlock).delete()
    db.query(RecognitionLocation).delete()
    db.query(Message).delete()
    db.query(ApprovedTheme).delete()
    db.query(Theme).delete()
    db.query(ApprovedLocation).delete()
    db.query(Location).delete()
    db.query(ApprovedBlock).delete()
    db.query(Block).delete()
    db.query(Document).delete()
    db.commit()
    return None

    
