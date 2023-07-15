from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from sqlalchemy.ext.hybrid import hybrid_property
from geoalchemy2.elements import WKBElement
from db.base_class import Base

# def wkb_to_shape(wkb: Union[WKBElement, BaseGeometry]) -> Optional[BaseGeometry]:
#     if isinstance(wkb, WKBElement):
#         return geoalchemy2.shape.to_shape(wkb)
#     elif isinstance(wkb, BaseGeometry):
#         return wkb
#     else:
#         return None


class Location(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    name = Column(String)
    geometry = Column(Geometry(), index=False)


class RecognitionLocation(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    probability = Column(Float)

    location_id = Column(UUID(as_uuid=True), ForeignKey('location.id'))
    location = relationship('Location')

    message_id = Column(UUID(as_uuid=True), ForeignKey('message.id'))
    message = relationship('Message', back_populates="recognition_locations")

    @hybrid_property
    def street_name(self):
        return self.location.name
    
    @hybrid_property
    def geometry(self):
        if self.Location.geometry:
            shape = to_shape(self.location.geometry)
            # print(shape.coords)
            geom = {
                "type": shape.geom_type,
                "coordinates": list(shape.coords)[0]
            }
            print(geom)
            
            # getattr(wkb_to_shape(self.location.geometry), "__geo_interface__", None)
            return geom
        return None


class ApprovedLocation(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    
    location_id = Column(UUID(as_uuid=True), ForeignKey('location.id'))
    location = relationship('Location')
    
    message = relationship('Message', back_populates='location')
    

