from typing import Optional, Union, Any
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from geojson_pydantic.geometries import Geometry, Point
from models.document import DocumentStatus

# from schemas.markup import Markup



class Location(BaseModel):
    name: Optional[str]
    geometry: Any

    class Config:
        orm_mode = True


class RecognitionLocationBase(BaseModel):
    probability: Optional[float]


class RecognitionLocationCreate(RecognitionLocationBase):
    message_id: UUID
    name: Optional[str]
    geometry: Optional[str]


class RecognitionLocation(RecognitionLocationBase):
    geometry: Optional[Any]
    street_name: Optional[str]

    class Config:
        orm_mode = True


class ApprovedLocationCreate(BaseModel):
    message_id: UUID
    name: Optional[str] #Location.name
    geometry: str #Location.geometry


class ApprovedLocation(BaseModel):
    name: str #Location.name
    geometry: str #Location.geometry


