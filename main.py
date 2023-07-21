from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from api.api_v1.api import api_router
from contextlib import asynccontextmanager
import logging 
import torch
from services.SOIKA.factfinder import TextClassifier, Geocoder, EventDetection

logger = logging.getLogger("gunicorn.error")

origins = [
    "http://localhost:3000",
    "https://nirma.lok-labs.com",
]

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Start model loading")
    device_type = torch.device('cpu')
    ml_models["blocks_model"] = TextClassifier(
        repository_id="Sandrro/text_to_function_v2",
        number_of_categories=3,
        device_type=device_type,
    )
    ml_models["themes_model"] =  TextClassifier(
        repository_id="Sandrro/text_to_subfunction_v10",
        number_of_categories=3,
        device_type=device_type,
    )
    # ml_models["address_model"] = Geocoder()

    ml_models["event_model"] = EventDetection()
    logger.info("Models loaded")
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

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
    from models.events import Events
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
    db.query(Events).delete()
    db.query(Document).delete()
    db.commit()
    return None

    
