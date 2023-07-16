from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from sqlalchemy.orm import relationship

from db.base_class import Base

from sqlalchemy.ext.hybrid import hybrid_property


    

class Message(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created_at = Column(DateTime)
    text = Column(String)
    
    document_id = Column(UUID(as_uuid=True), ForeignKey('document.id'))
    document = relationship('Document', back_populates='messages')
    
    recognition_blocks = relationship("RecognitionBlock", back_populates = "message", cascade="all, delete")
    recognition_themes = relationship("RecognitionTheme", back_populates = "message", cascade="all, delete")
    recognition_locations = relationship("RecognitionLocation", back_populates = "message", cascade="all, delete")


    block_id = Column(UUID(as_uuid=True), ForeignKey('approvedblock.id'))
    block = relationship('ApprovedBlock', back_populates="message", uselist=False, cascade="all, delete")
    theme_id = Column(UUID(as_uuid=True), ForeignKey('approvedtheme.id'))
    theme = relationship('ApprovedTheme', back_populates="message", uselist=False, cascade="all, delete")
    location_id = Column(UUID(as_uuid=True), ForeignKey('approvedlocation.id'))
    location = relationship('ApprovedLocation', back_populates="message", uselist=False, cascade="all, delete")

    @hybrid_property
    def approved_block(self):
        if self.block_id:
            # print(self.block)
            return self.block.block.name
        print("block_not_found")
        return None
    
    @hybrid_property
    def approved_theme(self):
        if self.theme:
            return self.theme.theme.name
        return None
    
    @hybrid_property
    def approved_location(self):
        try:
            from geoalchemy2.shape import to_shape
            return {"street_name": self.location.location.name, "geometry": to_shape(self.location.location.geometry).wkt}
        except:
            return None
    
from geoalchemy2.elements import WKBElement