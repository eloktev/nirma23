from typing import Any, Dict, Optional, Union, List
from uuid import UUID
from sqlalchemy.orm import Session
from shapely.wkt import loads
from dao.base import BaseDAO
from models.location import Location, RecognitionLocation, ApprovedLocation
from schemas.location import (Location as LocationSchema,
                           RecognitionLocationCreate,
                           ApprovedLocation as ApprovedLocationSchema,
                           ApprovedLocationCreate)

from geoalchemy2.shape import from_shape


class LocationDAO(BaseDAO[Location, LocationSchema, LocationSchema]):

    def create(self, db: Session, *, obj_in: LocationSchema) -> Location:
        location_obj = Location(
            geometry = obj_in.geometry,
            name = obj_in.name
        )
        db.add(location_obj)
        db.commit()
        db.refresh(location_obj)
        return location_obj


_dao_location = LocationDAO(Location)


class RecognitionLocationDAO(BaseDAO[RecognitionLocation, RecognitionLocationCreate, RecognitionLocationCreate]):

    def create(self, db: Session, *, obj_in: RecognitionLocationCreate) -> RecognitionLocation:
        # print(type(loads(obj_in.geometry))
        from geoalchemy2.shape import from_shape
        if obj_in.geometry:
            shape = loads(obj_in.geometry)
            geometry = from_shape(shape)
        else:
            geometry=None
        location_schematized = LocationSchema(name = obj_in.name, geometry=geometry)
        location = _dao_location.create(db, obj_in = location_schematized)
        
        location = RecognitionLocation(
            location=location,
            message_id=obj_in.message_id,
            probability = obj_in.probability
        )
        db.add(location)
        db.commit()
        db.refresh(location)
        return location


dao_location = RecognitionLocationDAO(RecognitionLocation) 

class ApprovedLocationDAO(BaseDAO[ApprovedLocation, ApprovedLocationCreate, ApprovedLocationCreate]):
    
    # def get_by_message_id(self,  db: Session, *, name: str) -> List[Optional[RecognitionBlock]]:
    #     return db.query(self.model).filter(self.model.name == name).first()

    def create(self, db: Session, *, obj_in: ApprovedLocationCreate):
        from geoalchemy2.shape import from_shape
        if obj_in.geometry:
            shape = loads(obj_in.geometry)
            geometry = from_shape(shape)
        else:
            geometry = None
        location_schematized = LocationSchema(name = obj_in.name, geometry=geometry)
        location = _dao_location.create(db, obj_in = location_schematized)
        a_location = ApprovedLocation(
            location_id=location.id,
        )
        db.add(a_location)
        db.commit()
        db.refresh(a_location)

        from dao.message import dao_message
        msg = dao_message.set_approved_location(db, message_id=obj_in.message_id, approved_location_id=a_location.id)
        return msg
    

dao_approvedlocation = ApprovedLocationDAO(ApprovedLocation) 